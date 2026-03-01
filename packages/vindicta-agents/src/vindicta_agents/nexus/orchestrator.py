from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from contextlib import asynccontextmanager

from ..utils.logger import logger
from ..telemetry.monitor import HardwareMonitor
from ..governor.resource_manager import ResourceGovernor
from ..governor.models import PriorityLevel
from .models import WARScribeEnvelope, AgentRegistry

# Initialize Telemetry & Governor
monitor = HardwareMonitor()
governor = ResourceGovernor(monitor)


@asynccontextmanager
async def lifespan(app: FastAPI):
    monitor.start()
    logger.info("nexus_startup", monitor_status="started")
    yield
    monitor.stop()
    logger.info("nexus_shutdown", monitor_status="stopped")


# Nexus Application
app = FastAPI(lifespan=lifespan)
registry = AgentRegistry()


@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    # 1. Resource Check (Handshake Phase)
    decision = governor.check_resources(PriorityLevel.NORMAL)
    if decision.should_throttle:
        await websocket.accept()
        await websocket.send_text(
            json.dumps(
                {
                    "error": "THROTTLED",
                    "reason": decision.reason,
                    "wait_time": decision.suggested_wait_time,
                }
            )
        )
        await websocket.close()
        logger.warning("handshake_throttled", agent_id=agent_id, reason=decision.reason)
        return

    await registry.connect(agent_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                envelope_dict = json.loads(data)
                envelope = WARScribeEnvelope(**envelope_dict)

                logger.info(
                    "message_received",
                    sender=agent_id,
                    action=envelope.action,
                    trace_id=envelope.trace_id,
                )

                response = {
                    "trace_id": envelope.trace_id,
                    "sender": "Nexus",
                    "receiver": agent_id,
                    "action": "ACK",
                    "payload": {"status": "Received"},
                }
                await registry.send_personal_message(json.dumps(response), agent_id)

            except Exception as e:
                logger.error("message_process_error", agent_id=agent_id, error=str(e))
                error_response = {"error": str(e)}
                await registry.send_personal_message(
                    json.dumps(error_response), agent_id
                )

    except WebSocketDisconnect:
        registry.disconnect(agent_id)


def start_nexus(host: str = "0.0.0.0", port: int = 8000):
    """Starts the Nexus Orchestrator."""
    import uvicorn

    uvicorn.run(app, host=host, port=port)

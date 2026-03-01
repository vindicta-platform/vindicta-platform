from pydantic import BaseModel, PrivateAttr
from typing import Optional, Any, Literal
import uuid
import json

from ..telemetry.models import ResourceUsage
from ..governor.models import PriorityLevel
from ..utils.logger import logger


class ResourceRequirements(BaseModel):
    priority: PriorityLevel = PriorityLevel.NORMAL
    estimated_usage: ResourceUsage


class BaseAgent(BaseModel):
    """
    BaseAgent class responsible for the Handshake Protocol.
    """

    agent_id: str
    agent_class: str
    realm: str
    status: Literal["Offline", "Online", "Busy", "Connected", "Connection Failed"] = (
        "Offline"
    )
    resources: Optional[ResourceRequirements] = None
    _websocket: Any = PrivateAttr(default=None)

    def handshake(self) -> bool:
        """
        Initiates the handshake with the Nexus (simulated).
        """
        if not self.realm:
            logger.warning(
                "handshake_failed", agent_id=self.agent_id, reason="missing_realm"
            )
            return False

        self.status = "Online"
        logger.info("handshake_success", agent_id=self.agent_id)
        return True

    async def connect_to_nexus(self, nexus_url: str = "ws://localhost:8000/ws"):
        """
        Connects the agent to the Nexus Orchestrator via WebSocket.
        """
        try:
            import websockets

            uri = f"{nexus_url}/{self.agent_id}"
            self._websocket = await websockets.connect(uri)
            self.status = "Connected"
            logger.info("nexus_connected", agent_id=self.agent_id, uri=uri)
        except ImportError:
            logger.error(
                "missing_dependency", library="websockets", agent_id=self.agent_id
            )
        except Exception as e:
            logger.error(
                "nexus_connection_failed", agent_id=self.agent_id, error=str(e)
            )
            self.status = "Connection Failed"

    async def send_envelope(self, action: str, payload: dict) -> None:
        """
        Sends a WARScribeEnvelope to the Nexus.
        """
        if not self._websocket:
            logger.warning(
                "message_send_skip", agent_id=self.agent_id, reason="not_connected"
            )
            return

        envelope = {
            "trace_id": str(uuid.uuid4()),
            "sender": self.agent_id,
            "action": action,
            "payload": payload,
        }

        try:
            await self._websocket.send(json.dumps(envelope))
            # Wait for ACK
            response = await self._websocket.recv()
            logger.info(
                "nexus_ack_received",
                agent_id=self.agent_id,
                action=action,
                response=response,
            )
        except Exception as e:
            logger.error("message_send_failed", agent_id=self.agent_id, error=str(e))

    async def close(self):
        if self._websocket:
            await self._websocket.close()
            self.status = "Offline"
            logger.info("nexus_connection_closed", agent_id=self.agent_id)

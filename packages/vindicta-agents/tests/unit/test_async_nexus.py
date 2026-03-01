import pytest
from vindicta_agents.nexus.orchestrator import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_async_boot_sequence():
    """
    Test that the AsyncNexus (represented by the FastAPI app) can handle async requests.
    Since TestClient is synchronous, we are testing the underlying async handlers.
    """
    # This is a bit meta because TestClient wraps async app in sync calls.
    # To truly test async loop, we'd need a running uvicorn instance or httpx.AsyncClient.
    # For now, we verify the websocket endpoint is accessible.
    with client.websocket_connect("/ws/async-test-agent") as websocket:
        envelope = {"sender": "async-test-agent", "action": "BOOT_CHECK", "payload": {}}
        websocket.send_json(envelope)
        response = websocket.receive_json()
        assert response["action"] == "ACK"


@pytest.mark.asyncio
async def test_json_rpc_envelope_validation():
    """
    Verify strict envelope schema validation.
    """
    with client.websocket_connect("/ws/validator-agent") as websocket:
        # Missing 'action' field
        bad_envelope = {"sender": "validator-agent", "payload": {}}
        websocket.send_json(bad_envelope)
        response = websocket.receive_json()
        assert "error" in response

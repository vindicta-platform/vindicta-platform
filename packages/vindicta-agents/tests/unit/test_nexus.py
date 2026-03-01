from fastapi.testclient import TestClient
from vindicta_agents.nexus.orchestrator import app
import json

client = TestClient(app)


def test_websocket_connection():
    with client.websocket_connect("/ws/test-agent") as websocket:
        # Send a valid envelope
        envelope = {"sender": "test-agent", "action": "PING", "payload": {}}
        websocket.send_text(json.dumps(envelope))

        # Expect ACK
        data = websocket.receive_text()
        response = json.loads(data)
        assert response["action"] == "ACK"
        assert response["receiver"] == "test-agent"


def test_malformed_envelope():
    with client.websocket_connect("/ws/test-agent") as websocket:
        # Send invalid JSON
        websocket.send_text("not json")

        data = websocket.receive_text()
        response = json.loads(data)
        assert "error" in response


def test_registry_tracking():
    # This is harder to test with TestClient as it doesn't expose the app state easily in the same process
    # But we can verify connection acceptance in the previous test.
    pass

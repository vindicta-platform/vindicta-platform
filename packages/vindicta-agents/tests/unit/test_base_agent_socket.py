import pytest
from unittest.mock import AsyncMock, patch
from vindicta_agents.core.base_agent import BaseAgent
import json


@pytest.mark.asyncio
async def test_agent_connect_success():
    """
    Test successful connection to Nexus (Mocked).
    """
    agent = BaseAgent(
        agent_id="mock-agent", agent_class="UnitTester", realm="test-realm"
    )

    with patch("websockets.connect", new_callable=AsyncMock) as mock_connect:
        mock_ws = AsyncMock()
        mock_connect.return_value = mock_ws

        await agent.connect_to_nexus("ws://mock-nexus")

        assert agent.status == "Connected"
        mock_connect.assert_called_once_with("ws://mock-nexus/mock-agent")


@pytest.mark.asyncio
async def test_agent_connect_failure():
    """
    Test connection failure handled gracefully.
    """
    agent = BaseAgent(
        agent_id="mock-agent", agent_class="UnitTester", realm="test-realm"
    )

    with patch("websockets.connect", side_effect=Exception("Connection Refused")):
        await agent.connect_to_nexus("ws://mock-nexus")

        assert agent.status == "Connection Failed"


@pytest.mark.asyncio
async def test_agent_send_envelope():
    """
    Test sending a message (envelope) via WebSocket.
    """
    agent = BaseAgent(
        agent_id="mock-agent", agent_class="UnitTester", realm="test-realm"
    )
    agent.status = "Connected"

    # Mock the internal websocket object
    mock_ws = AsyncMock()
    # Mock recv for ACK
    mock_ws.recv.return_value = json.dumps({"status": "ACK"})

    # Inject mock websocket (using PrivateAttr workaround or direct access if allowed in test)
    # Using direct access since we are in python and _websocket is just an attribute
    agent._websocket = mock_ws

    payload = {"foo": "bar"}
    await agent.send_envelope(action="TEST", payload=payload)

    # Verify send called with JSON
    assert mock_ws.send.called
    args, _ = mock_ws.send.call_args
    sent_msg = json.loads(args[0])

    assert sent_msg["sender"] == "mock-agent"
    assert sent_msg["action"] == "TEST"
    assert sent_msg["payload"] == payload
    assert "trace_id" in sent_msg

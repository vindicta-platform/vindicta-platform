import pytest
from pydantic import ValidationError

try:
    from vindicta_agents.core.base_agent import BaseAgent
except ImportError:
    pytest.fail("Could not import BaseAgent module")


def test_base_agent_initialization():
    """Test validation of BaseAgent attributes."""
    agent = BaseAgent(
        agent_id="test-agent-1", agent_class="Tech-Priest", realm="vindicta-engine"
    )
    assert agent.agent_class == "Tech-Priest"
    assert agent.realm == "vindicta-engine"
    assert agent.status == "Offline"  # Default status


def test_base_agent_missing_realm():
    """Test failure when realm is missing."""
    with pytest.raises(ValidationError):
        BaseAgent(agent_id="test-agent-2", agent_class="Tech-Priest")


def test_handshake():
    """Test the handshake method."""
    agent = BaseAgent(
        agent_id="test-agent-3", agent_class="Logos-Historian", realm="platform-docs"
    )
    assert agent.handshake() == True
    assert agent.status == "Online"

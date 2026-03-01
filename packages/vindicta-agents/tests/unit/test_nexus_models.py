"""Tests for extracted Nexus models and NexusClient."""

import pytest
from vindicta_agents.nexus.models import WARScribeEnvelope, AgentRegistry
from vindicta_agents.nexus.client import NexusClient


class TestWARScribeEnvelope:
    def test_valid_envelope(self):
        env = WARScribeEnvelope(sender="agent-1", action="PING", payload={})
        assert env.sender == "agent-1"
        assert env.receiver == "Nexus"
        assert env.action == "PING"
        assert env.trace_id  # auto-generated UUID

    def test_custom_receiver(self):
        env = WARScribeEnvelope(
            sender="agent-1",
            receiver="TechPriest",
            action="DELEGATE",
            payload={"task": "x"},
        )
        assert env.receiver == "TechPriest"

    def test_envelope_with_payload(self):
        payload = {"target_realm": "vindicta-engine", "priority": "high"}
        env = WARScribeEnvelope(sender="agent-1", action="EXECUTE", payload=payload)
        assert env.payload["target_realm"] == "vindicta-engine"

    def test_envelope_missing_required_fields(self):
        with pytest.raises(Exception):
            WARScribeEnvelope(payload={})  # missing sender and action


class TestAgentRegistry:
    def test_initial_state(self):
        registry = AgentRegistry()
        assert registry.connected_agents == []
        assert len(registry.active_connections) == 0

    def test_disconnect_nonexistent_agent(self):
        """Should not raise on disconnecting unknown agent."""
        registry = AgentRegistry()
        registry.disconnect("ghost-agent")  # no-op, no crash


class TestNexusClient:
    def test_client_creation(self):
        client = NexusClient("ws://localhost:9000")
        assert client.nexus_url == "ws://localhost:9000"

    def test_default_url(self):
        client = NexusClient()
        assert client.nexus_url == "ws://localhost:8000"

    @pytest.mark.asyncio
    async def test_report_activation(self):
        """Ensure report_activation runs without error (log-only stub)."""
        client = NexusClient()
        await client.report_activation("TechPriest", "trace-123")

    @pytest.mark.asyncio
    async def test_report_completion(self):
        client = NexusClient()
        await client.report_completion("TechPriest", "trace-123", {"status": "done"})

    @pytest.mark.asyncio
    async def test_report_error(self):
        client = NexusClient()
        await client.report_error("TechPriest", "trace-123", "Something broke")

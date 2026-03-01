"""
Nexus Client
=============
Lightweight async client for swarm nodes to optionally report
status to a running Nexus server. Designed for injection via
RunnableConfig["configurable"]["nexus_client"].

Usage:
    client = NexusClient("ws://localhost:8000")
    await client.report_activation("TechPriest", trace_id)
"""

from typing import Any, Dict

from ..utils.logger import logger


class NexusClient:
    """Async client for communicating with the Nexus control plane."""

    def __init__(self, nexus_url: str = "ws://localhost:8000") -> None:
        self.nexus_url = nexus_url
        self._connected = False

    async def report_activation(self, agent_name: str, trace_id: str) -> None:
        """Report that a domain agent node has been activated."""
        logger.info(
            "nexus_client_report",
            report_type="activation",
            agent=agent_name,
            trace_id=trace_id,
            nexus_url=self.nexus_url,
        )
        # Future: open websocket, send WARScribeEnvelope
        # For now, log-only — actual connection deferred to service split

    async def report_completion(
        self, agent_name: str, trace_id: str, result: Dict[str, Any]
    ) -> None:
        """Report that a domain agent node has completed execution."""
        logger.info(
            "nexus_client_report",
            report_type="completion",
            agent=agent_name,
            trace_id=trace_id,
        )

    async def report_error(self, agent_name: str, trace_id: str, error: str) -> None:
        """Report that a domain agent node encountered an error."""
        logger.error(
            "nexus_client_report",
            report_type="error",
            agent=agent_name,
            trace_id=trace_id,
            error=error,
        )

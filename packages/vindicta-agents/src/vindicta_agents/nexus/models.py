"""
Nexus Data Models
=================
Shared data models for the Nexus control plane, extracted from
orchestrator.py so they can be imported independently by clients
and other services.
"""

import uuid
from typing import Any, Dict

from fastapi import WebSocket
from pydantic import BaseModel, Field

from ..utils.logger import logger


class WARScribeEnvelope(BaseModel):
    """Standard Envelope for all Swarm Communication."""

    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str
    receiver: str = "Nexus"
    action: str
    payload: Dict[str, Any]


class AgentRegistry:
    """Tracks active agents and their WebSocket connections."""

    def __init__(self) -> None:
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, agent_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[agent_id] = websocket
        logger.info("agent_connected", agent_id=agent_id)

    def disconnect(self, agent_id: str) -> None:
        if agent_id in self.active_connections:
            del self.active_connections[agent_id]
            logger.info("agent_disconnected", agent_id=agent_id)

    async def send_personal_message(self, message: str, agent_id: str) -> None:
        if agent_id in self.active_connections:
            await self.active_connections[agent_id].send_text(message)

    @property
    def connected_agents(self) -> list[str]:
        return list(self.active_connections.keys())

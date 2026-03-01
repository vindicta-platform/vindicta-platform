from typing import Any, Optional
from abc import ABC, abstractmethod
from pydantic import Field
from vindicta_foundation.models.base import VindictaModel


class BaseTacticalDecision(VindictaModel):
    """Base model for a tactical decision made by an AI."""

    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in this decision"
    )
    reasoning: str = Field(..., description="Explanation of why this decision was made")
    action_type: str = Field(
        ..., description="Type of action (e.g., 'move', 'shoot', 'charge')"
    )
    target_id: Optional[str] = Field(
        None, description="Optional ID of the target unit/location"
    )


class BaseAIProfile(VindictaModel):
    """Configuration profile for an AI opponent."""

    name: str = Field(..., description="Name of the AI personality")
    aggression: float = Field(
        0.5, ge=0.0, le=1.0, description="Tendency to attack vs defend"
    )
    risk_tolerance: float = Field(
        0.5, ge=0.0, le=1.0, description="Willingness to take risks"
    )


class BaseTacticalEngine(ABC):
    """Abstract interface for AI decision making engines."""

    @abstractmethod
    def evaluate_state(self, game_state: Any) -> float:
        """Evaluate the current game state from the perspective of the active player."""
        pass

    @abstractmethod
    def decide_next_action(self, game_state: Any) -> BaseTacticalDecision:
        """Determine the next best action given the current state."""
        pass

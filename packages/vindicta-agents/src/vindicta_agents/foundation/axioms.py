from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class EntityIdentity(BaseModel):
    """
    AX-01: Entity Identity
    Every object must have a unique, immutable UUID. State is a function of time.
    """

    id: UUID = Field(default_factory=uuid4, frozen=True)
    created_at: datetime = Field(default_factory=datetime.now)


class Dimensionality(BaseModel):
    """
    AX-02: Dimensionality
    All coordinates exist in a 3D Euclidean space (44x60" bounds).
    Negative X/Y is a "Constitutional Violation."
    """

    x: float
    y: float
    z: float = 0.0

    @field_validator("x")
    @classmethod
    def validate_x(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Constitutional Violation: Negative X coordinate")
        if v > 44:
            raise ValueError(
                "Constitutional Violation: X coordinate out of bounds (Max 44)"
            )
        return v

    @field_validator("y")
    @classmethod
    def validate_y(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Constitutional Violation: Negative Y coordinate")
        if v > 60:
            raise ValueError(
                "Constitutional Violation: Y coordinate out of bounds (Max 60)"
            )
        return v


class ProbabilitySource(BaseModel):
    """
    AX-03: Probability Source
    All random outcomes must be traceable to a central Entropy Provider (The Die).
    """

    provider_id: str
    seed: Optional[int] = None


class TemporalDiscretization(BaseModel):
    """
    AX-04: Temporal Discretization
    The system operates in discrete steps (Phases).
    """

    current_phase: int

    @field_validator("current_phase")
    @classmethod
    def validate_phase(cls, v: int) -> int:
        if not isinstance(v, int):
            raise ValueError("Constitutional Violation: Phase must be an integer")
        return v


# First-Order Postulates (Placeholders for now, or minimal implementation)
class Translation(BaseModel):
    vector: Dimensionality


class Interaction(BaseModel):
    target_id: UUID
    range: float


class Unity(BaseModel):
    entity_id: UUID
    footprint: Dimensionality

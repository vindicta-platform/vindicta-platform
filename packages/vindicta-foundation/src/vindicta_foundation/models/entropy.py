from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4
from pydantic import Field, field_validator

from vindicta_foundation.models.base import VindictaModel


class EntropyProof(VindictaModel):
    """Cryptographically verifiable proof for mechanical actions.

    Constitutional Compliance:
    - Rule VII: No probabilistic AI. All randomness must be traceable.
    """

    seed_hash: str = Field(..., description="SHA-256 hash of the entropy seed")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Time of entropy generation",
    )
    algorithm: Literal["csprng", "rejection_sampling"] = Field(
        default="csprng", description="The method used to generate entropy"
    )
    audit_trail_id: UUID = Field(
        default_factory=uuid4, description="Link to the audit log for this random event"
    )

    @field_validator("seed_hash")
    @classmethod
    def validate_seed_hash(cls, v: str) -> str:
        """Validates that the provided seed hash is a valid SHA-256 digest.

        Args:
            v (str): The string value to validate.

        Returns:
            str: The validated SHA-256 string.

        Raises:
            ValueError: If the string is empty or less than 64 characters.
        """
        if not v or len(v) < 64:
            raise ValueError("Invalid seed hash: must be SHA-256 hex digest")
        return v

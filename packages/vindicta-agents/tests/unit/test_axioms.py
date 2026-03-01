import pytest
import uuid
from datetime import datetime
from pydantic import ValidationError

# Verify that the module can be imported (will fail initially)
from vindicta_agents.foundation.axioms import (
    EntityIdentity,
    Dimensionality,
    ProbabilitySource,
    TemporalDiscretization,
)


def test_entity_identity_valid():
    """Test that EntityIdentity creates a valid UUID and timestamp."""
    entity = EntityIdentity()
    assert isinstance(entity.id, uuid.UUID)
    assert isinstance(entity.created_at, datetime)


def test_dimensionality_valid():
    """Test valid coordinates."""
    # 44x60 bounds, so (10, 20, 0) is valid
    dim = Dimensionality(x=10.0, y=20.0, z=0.0)
    assert dim.x == 10.0
    assert dim.y == 20.0
    assert dim.z == 0.0


def test_dimensionality_negative_coordinates():
    """Test that negative coordinates raise ValidationError."""
    with pytest.raises(ValidationError):
        Dimensionality(x=-5.0, y=10.0, z=0.0)


def test_dimensionality_out_of_bounds():
    """Test that out of bounds coordinates raise ValidationError."""
    # X max is 44, Y max is 60
    with pytest.raises(ValidationError):
        Dimensionality(x=45.0, y=10.0, z=0.0)

    with pytest.raises(ValidationError):
        Dimensionality(x=10.0, y=61.0, z=0.0)


def test_probability_source():
    """Test that ProbabilitySource references a provider."""
    prob = ProbabilitySource(provider_id="central-entropy")
    assert prob.provider_id == "central-entropy"


def test_temporal_discretization():
    """Test discrete phases."""
    phase = TemporalDiscretization(current_phase=1)
    assert phase.current_phase == 1

    # Should not accept floats for integer phases if strict
    # Pydantic might coerce float to int, but logic should handle it.
    # Here we just check basic assignment.

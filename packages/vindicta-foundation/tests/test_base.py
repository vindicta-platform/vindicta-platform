import pytest
from uuid import UUID
from datetime import datetime
from vindicta_foundation.models.base import VindictaModel


def test_vindicta_model_defaults() -> None:
    """Test the default values when instantiating a bare VindictaModel."""
    model = VindictaModel()
    assert isinstance(model.id, UUID)
    assert isinstance(model.created_at, datetime)
    assert model.updated_at is None


def test_vindicta_model_serialization() -> None:
    """Test model serialization to dict and JSON."""
    model = VindictaModel()
    model_dict = model.model_dump()
    assert "id" in model_dict
    assert "created_at" in model_dict

    model_json = model.model_dump_json()
    assert str(model.id) in model_json


def test_vindicta_model_field_validation() -> None:
    """Test field validation and assignment."""
    model = VindictaModel()
    new_id = UUID("12345678-1234-5678-1234-567812345678")
    model.id = new_id
    assert model.id == new_id

    # Test edge case: invalid assignment type (should raise validation error)
    with pytest.raises(ValueError):
        model.id = "not-a-uuid"  # type: ignore

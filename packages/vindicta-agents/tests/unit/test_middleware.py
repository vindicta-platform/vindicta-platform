import pytest

# Mocking the models for test purposes if not importable, but we expect them to be
try:
    from vindicta_agents.foundation.axioms import Dimensionality
    from vindicta_agents.core.middleware import validate_intent
except ImportError:
    pytest.fail("Could not import middleware or axioms")


def test_validate_intent_valid():
    """Test that valid intents pass."""

    # Mocking a WARScribeEntry-like object
    class MockIntent:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    intent = MockIntent(10.0, 20.0)
    # Validation should succeed (return True or None)
    assert validate_intent(intent) is True


def test_validate_intent_invalid_coords():
    """Test that invalid coordinates raise a violation."""

    class MockIntent:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    intent = MockIntent(-5.0, 20.0)
    with pytest.raises(ValueError, match="Constitutional Violation"):
        validate_intent(intent)

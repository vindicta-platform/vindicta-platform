from typing import Any
from vindicta_agents.foundation.axioms import Dimensionality


def validate_intent(intent: Any) -> bool:
    """
    Constitutional Middleware: Checks any proposed move against the Axioms.

    Args:
        intent: A WARScribeEntry or compatible object with x/y/z attributes.

    Returns:
        bool: True if valid, raises ValueError (Constitutional Violation) otherwise.
    """
    # Axiom 02: Dimensionality Check
    if hasattr(intent, "x") and hasattr(intent, "y"):
        # We use the Pydantic model to validate the values
        # If it initiates without error, it's valid.
        z = getattr(intent, "z", 0.0)
        Dimensionality(x=intent.x, y=intent.y, z=z)

    # Additional checks can be added here

    return True

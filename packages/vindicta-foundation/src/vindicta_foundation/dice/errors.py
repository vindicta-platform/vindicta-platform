"""Error types for the dice-core module."""


class SecurityError(Exception):
    """Raised when a cryptographic security constraint is violated.

    Specifically, this is raised if a deterministic seed is provided
    in PRODUCTION mode, which would compromise the integrity of the
    CSPRNG output.
    """

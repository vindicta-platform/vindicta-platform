import pytest
from uuid import UUID
from datetime import datetime
from vindicta_foundation.models.entropy import EntropyProof


def test_entropy_proof_validation() -> None:
    """Test valid and invalid entropy proof seed hashes."""
    # Valid SHA-256 hash
    valid_hash = "a" * 64
    proof = EntropyProof(seed_hash=valid_hash)
    assert proof.algorithm == "csprng"
    assert isinstance(proof.timestamp, datetime)
    assert isinstance(proof.audit_trail_id, UUID)

    # Invalid hash
    with pytest.raises(ValueError):
        EntropyProof(seed_hash="short")


def test_entropy_proof_algorithm_validation() -> None:
    """Test algorithm literal validation."""
    valid_hash = "b" * 64
    proof = EntropyProof(seed_hash=valid_hash, algorithm="rejection_sampling")
    assert proof.algorithm == "rejection_sampling"

    # Invalid algorithm
    with pytest.raises(ValueError):
        EntropyProof(seed_hash=valid_hash, algorithm="invalid_alg")  # type: ignore

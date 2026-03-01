import pytest
from unittest.mock import patch

try:
    from vindicta_agents.utils.discovery import find_meso_repos
except ImportError:
    pytest.fail("Could not import discovery module")


@patch("os.path.exists")
@patch("os.path.isdir")
def test_find_meso_repos_success(mock_isdir, mock_exists):
    """Test identifying all repos when they exist."""
    # Mock that all looked-up paths exist
    mock_exists.return_value = True
    mock_isdir.return_value = True

    # We need to mock the root path or how the function determines it.
    # Assuming the function uses CWD or a relative path from the verified Agent location.

    repos = find_meso_repos("c:/Users/bfoxt/vindicta-platform")

    assert "vindicta-foundation" in repos
    assert "vindicta-engine" in repos
    assert repos["vindicta-foundation"]["status"] == "verified"


@patch("os.path.exists")
def test_find_meso_repos_missing(mock_exists):
    """Test identifying missing repos."""

    # Mock that some exist and others don't
    def side_effect(path):
        if "vindicta-engine" in path:
            return False
        return True

    mock_exists.side_effect = side_effect

    repos = find_meso_repos("c:/Users/bfoxt/vindicta-platform")

    assert "vindicta-engine" in repos
    assert repos["vindicta-engine"]["status"] == "missing"
    assert repos["vindicta-foundation"]["status"] == "verified"

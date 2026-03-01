import os
from typing import Dict

MESO_REPOS = [
    "vindicta-foundation",
    "vindicta-agents",
    "vindicta-engine",
    "vindicta-oracle",
    "vindicta-economy",
    "vindicta-portal",
    "warscribe-system",  # Or platform-core? The prompt listed 7. I'll stick to the approved plan list.
]


def find_meso_repos(root_path: str = None) -> Dict[str, Dict[str, str]]:
    """
    Detects the presence of meso-repositories in the sibling directories.
    If root_path is not provided, it assumes the parent of the current repo.
    """
    if not root_path:
        # Assuming we are in src/vindicta_agents/utils/discovery.py
        # .../Vindicta-Agents/src/vindicta_agents/utils/discovery.py
        # root is .../
        # But for robustness, we might expect an env var or the user to pass it.
        # Let's fallback to CWD's parent if not found.
        root_path = os.path.abspath(os.path.join(os.getcwd(), ".."))

    results = {}

    for repo in MESO_REPOS:
        repo_path = os.path.join(root_path, repo)
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            results[repo] = {"path": repo_path, "status": "verified"}
        else:
            results[repo] = {"path": repo_path, "status": "missing"}

    return results

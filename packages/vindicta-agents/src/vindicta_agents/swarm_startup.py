"""
Swarm Startup Script
====================
Initializes the Nexus Control Plane and verifies all meso-repos are reachable.

Usage:
    uv run python -m vindicta_agents.swarm_startup
"""

import os
from vindicta_agents.utils.discovery import find_meso_repos
from vindicta_agents.core.base_agent import BaseAgent


BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║          VINDICTA SWARM CONTROL PLANE v0.1.0                ║
║          Codename: "The Nexus"                              ║
╚══════════════════════════════════════════════════════════════╝
"""


def boot_nexus(platform_root: str | None = None) -> dict:
    """
    Boot the Nexus Control Plane.

    1. Discover meso-repos.
    2. Register the Architect Agent.
    3. Report status.
    """
    print(BANNER)

    # Step 1: Discover meso-repos
    if not platform_root:
        # Default: assume we are inside Vindicta-Agents, go up one level
        platform_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

    print(f"[NEXUS] Platform root: {platform_root}")
    print("[NEXUS] Scanning for meso-repositories...\n")

    repos = find_meso_repos(platform_root)

    verified = 0
    missing = 0
    for name, info in repos.items():
        status_icon = "✓" if info["status"] == "verified" else "✗"
        print(f"  {status_icon} {name:30s} [{info['status'].upper()}]")
        if info["status"] == "verified":
            verified += 1
        else:
            missing += 1

    print(f"\n[NEXUS] Repos verified: {verified}/{len(repos)}")

    if missing > 0:
        print(f"[NEXUS] WARNING: {missing} repo(s) missing. Swarm incomplete.")

    # Step 2: Register the Architect Agent
    architect = BaseAgent(
        agent_id="architect-001",
        agent_class="Architect",
        realm="vindicta-agents",
    )
    architect.handshake()
    print(
        f"\n[NEXUS] Architect Agent registered: {architect.agent_id} [{architect.status}]"
    )

    # Step 3: Report
    print("\n[NEXUS] ══════════════════════════════════════")
    if missing == 0:
        print("[NEXUS] STATUS: ALL SYSTEMS OPERATIONAL")
    else:
        print("[NEXUS] STATUS: PARTIAL — Missing repos detected")
    print("[NEXUS] ══════════════════════════════════════\n")

    return {
        "repos": repos,
        "architect": architect,
        "verified": verified,
        "missing": missing,
    }


if __name__ == "__main__":
    boot_nexus()

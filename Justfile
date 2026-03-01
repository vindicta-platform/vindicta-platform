# Vindicta Platform Root Commands

# Synchronize .agent rules from the platform root to all submodule packages
sync-agents:
    python scripts/sync_agents.py

# Synchronize .github/workflows from the platform root to all submodule packages
sync-workflows:
    python scripts/sync_workflows.py

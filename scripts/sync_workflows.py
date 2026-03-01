#!/usr/bin/env python3
"""
Sync GitHub Workflows across Submodules

This script ensures that specific GitHub Action workflows (like deploy-docs.yml)
are distributed to all submodules so they independently trigger CI/CD pipelines.
"""

import shutil
from pathlib import Path


def sync_workflows():
    # Define paths relative to the script location
    script_dir = Path(__file__).parent.resolve()
    platform_root = script_dir.parent

    source_workflow = platform_root / ".github" / "workflows" / "deploy-docs.yml"
    packages_dir = platform_root / "packages"

    if not source_workflow.exists():
        print(f"Error: Source workflow not found at {source_workflow}")
        return

    # Submodules to sync
    target_packages = [
        "vindicta-foundation",
        "vindicta-engine",
        "warscribe-system",
        "vindicta-economy",
        "vindicta-oracle",
        "vindicta-agents",
    ]

    for package_name in target_packages:
        package_path = packages_dir / package_name
        if not package_path.exists():
            print(f"Skipping {package_name}: Directory does not exist")
            continue

        dest_workflow_dir = package_path / ".github" / "workflows"
        dest_workflow_file = dest_workflow_dir / "deploy-docs.yml"

        print(f"Syncing deploy-docs.yml to {package_name}...")

        # Ensure destination directory exists
        dest_workflow_dir.mkdir(parents=True, exist_ok=True)

        # Copy file unconditionally (will override existing)
        shutil.copy2(source_workflow, dest_workflow_file)

    print("Workflow synchronization complete!")


if __name__ == "__main__":
    sync_workflows()

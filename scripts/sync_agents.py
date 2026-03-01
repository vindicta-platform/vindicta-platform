#!/usr/bin/env python3
"""
Sync Agent Configurations across Submodules

This script copies the `.agent` directory from the root of the platform
into all recognized submodule packages. It overwrites matching files but
does not delete unique files in the destination repositories.
"""

import os
import shutil
from pathlib import Path


def sync_agents():
    # Define paths relative to the script location
    script_dir = Path(__file__).parent.resolve()
    platform_root = script_dir.parent

    source_agent_dir = platform_root / ".agent"
    packages_dir = platform_root / "packages"

    if not source_agent_dir.exists():
        print(f"Error: Source agent directory not found at {source_agent_dir}")
        return

    if not packages_dir.exists():
        print(f"Error: Packages directory not found at {packages_dir}")
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
            print(
                f"Skipping {package_name}: Directory does not exist at {package_path}"
            )
            continue

        dest_agent_dir = package_path / ".agent"
        print(f"Syncing .agent to {package_name}...")

        # Ensure destination .agent directory exists
        dest_agent_dir.mkdir(exist_ok=True)

        # Walk through the source directory and copy files
        for root, dirs, files in os.walk(source_agent_dir):
            rel_path = Path(root).relative_to(source_agent_dir)
            dest_dir = dest_agent_dir / rel_path

            # Create directories in destination
            dest_dir.mkdir(parents=True, exist_ok=True)

            for file in files:
                src_file = Path(root) / file
                dst_file = dest_dir / file

                # Copy file unconditionally (will override existing)
                shutil.copy2(src_file, dst_file)
                # print(f"  Copied {rel_path / file}")

    print("Synchronization complete!")


if __name__ == "__main__":
    sync_agents()

import sys
import os
import subprocess
from typing import List

# Ensure src is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vindicta_agents.swarm.domain_registry import DOMAIN_REGISTRY


def run_cmd(cmd: List[str], cwd: str) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(f"Warning: Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout.strip()


def get_platform_root() -> str:
    # sibling to current repo
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    print("🧹 Cleaning up Swarm PRs (Removing ignored files)")

    platform_root = get_platform_root()

    # Get active PRs
    # We look for PRs with title "feat: Standardized Health Check"
    # across the repos.
    # Actually, we can just iterate domains and check active branch or query gh.

    for realm, info in DOMAIN_REGISTRY.items():
        repo_name = info["repo_name"]
        repo_path = os.path.join(platform_root, repo_name)

        if not os.path.exists(repo_path):
            print(f"Skipping {repo_name} (not found)")
            continue

        print(f"\nProcessing {repo_name}...")

        # 1. Find the PR branch
        # We assume local branch is still there from run_showcase.py execution
        # Or we can grep `git branch`
        branches = run_cmd(
            ["git", "branch", "--list", "feat/health-check*"], cwd=repo_path
        )
        if not branches:
            print("  No health-check branch found.")
            continue

        # Take the first one (should be only one)
        branch = branches.splitlines()[0].strip().replace("* ", "")
        print(f"  Found branch: {branch}")

        # Checkout
        run_cmd(["git", "checkout", branch], cwd=repo_path)

        # 2. Add .gitignore if missing
        ensure_gitignore(repo_path, info.get("package_name", "python"))  # heuristic

        # 3. Force Clean Index (The only way to be sure)
        print("  Purging index to respect .gitignore...")

        # Remove everything from index (files stay on disk)
        run_cmd(["git", "rm", "-r", "--cached", "."], cwd=repo_path)

        # Re-add everything (respecting the new .gitignore)
        run_cmd(["git", "add", "."], cwd=repo_path)

        # 4. Commit and Push
        status = run_cmd(["git", "status", "--porcelain"], cwd=repo_path)
        if status:
            print("  Committing fixes...")
            run_cmd(
                [
                    "git",
                    "commit",
                    "-m",
                    "fix: enforce .gitignore and remove ignored files",
                ],
                cwd=repo_path,
            )
            run_cmd(["git", "push"], cwd=repo_path)
            print("  ✅ Fix pushed.")
        else:
            print("  Index clean (nothing changed).")


def ensure_gitignore(repo_path: str, tech_hint: str):
    gitignore_path = os.path.join(repo_path, ".gitignore")

    defaults = [
        "__pycache__/",
        "*.pyc",
        ".DS_Store",
        ".env",
        "node_modules/",
        "coverage/",
        ".pytest_cache/",
        "dist/",
        "build/",
    ]

    if not os.path.exists(gitignore_path):
        print("  Creating .gitignore")
        with open(gitignore_path, "w") as f:
            f.write("\n".join(defaults))
    else:
        # Check if basic ignores exist, append if not?
        # For showcase, simple append is safe
        with open(gitignore_path, "r") as f:
            content = f.read()

        missing = [item for item in defaults if item not in content]
        if missing:
            print(f"  Updating .gitignore with {len(missing)} rules")
            with open(gitignore_path, "a") as f:
                f.write("\n" + "\n".join(missing))


if __name__ == "__main__":
    main()

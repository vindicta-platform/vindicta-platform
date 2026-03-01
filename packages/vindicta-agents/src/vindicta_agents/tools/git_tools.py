"""
Git Tools Module
================

Provides safe wrappers for Git and GitHub CLI operations to be used by Swarm Agents.
"""

import os
import subprocess
from typing import List

from ..utils.logger import logger


def run_cmd(cmd: List[str], cwd: str, sensitive_args: List[str] = None) -> str:
    """Executes a subprocess command and returns stdout."""
    try:
        if os.name == "nt":
            # On Windows, we need shell=True for some commands to be found if not in path correctly,
            # but usually purely list-based is safer. Using list based.
            # If standard executables are in PATH, it works.
            pass

        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(cmd)
        if sensitive_args:
            for arg in sensitive_args:
                cmd_str = cmd_str.replace(arg, "[REDACTED]")

        logger.error("command_failed", command=cmd_str, error=e.stderr)
        raise RuntimeError(f"Command failed: {e.stderr}")


def verify_repo_clean(repo_path: str) -> bool:
    """Checks if the repo has no uncommitted changes."""
    status = run_cmd(["git", "status", "--porcelain"], cwd=repo_path)
    return len(status) == 0


def checkout_new_branch(repo_path: str, branch_name: str) -> None:
    """Creates and checks out a new branch."""
    run_cmd(["git", "checkout", "-b", branch_name], cwd=repo_path)
    logger.info("branch_created", branch=branch_name, repo=repo_path)


def add_files(repo_path: str, files: List[str]) -> None:
    """Stages specific files."""
    run_cmd(["git", "add"] + files, cwd=repo_path)
    logger.info("files_staged", files=files)


def commit_files(
    repo_path: str,
    message: str,
    author_name: str = "Vindicta Bot",
    author_email: str = "bot@vindicta.ai",
    stage_all: bool = True,
) -> None:
    """Commits changes with the specified author. Optionally stages all changes first."""
    if stage_all:
        run_cmd(["git", "add", "."], cwd=repo_path)

    author_flag = f"{author_name} <{author_email}>"
    run_cmd(["git", "commit", "--author", author_flag, "-m", message], cwd=repo_path)
    logger.info("files_committed", message=message, author=author_flag)


def push_branch(repo_path: str, branch_name: str) -> None:
    """Pushes the current branch to origin."""
    run_cmd(["git", "push", "-u", "origin", branch_name], cwd=repo_path)
    logger.info("branch_pushed", branch=branch_name)


def create_pr(repo_path: str, title: str, body: str, reviewer: str) -> str:
    """Creates a PR using the gh CLI and returns the PR URL."""
    # Ensure gh is authenticated (assumed pre-check passed)
    cmd = [
        "gh",
        "pr",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--reviewer",
        reviewer,
    ]
    url = run_cmd(cmd, cwd=repo_path)
    logger.info("pr_created", url=url)
    return url


def write_file(repo_path: str, rel_path: str, content: str) -> None:
    """Writes content to a file in the repository."""
    full_path = os.path.join(repo_path, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("file_written", path=full_path)

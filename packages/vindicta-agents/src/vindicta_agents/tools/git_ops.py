"""Git operations — thin wrapper around GitPython.

Provides a ``GitWorkspace`` class that wraps ``git.Repo`` with a
simplified API for the operations agents need: branching, staging,
committing, pushing, and fetching.

Credentials are injected via environment variables:

* ``GIT_TOKEN`` — used to construct authenticated HTTPS remote URLs.
"""

from __future__ import annotations

from pathlib import Path

import git  # GitPython


class GitWorkspace:
    """Simplified Git operations scoped to a local repository.

    Parameters
    ----------
    path:
        Path to the root of a Git repository (must already be
        initialised).
    """

    def __init__(self, path: str | Path) -> None:
        self._repo = git.Repo(str(path))

    # ---- branch operations ----

    def checkout(self, branch: str, *, create: bool = False) -> None:
        """Switch to *branch*, optionally creating it first."""
        if create:
            self._repo.git.checkout("-b", branch)
        else:
            self._repo.git.checkout(branch)

    def branch_exists(self, name: str) -> bool:
        """Return ``True`` if a local branch called *name* exists."""
        return name in [ref.name for ref in self._repo.branches]  # type: ignore[union-attr]

    @property
    def active_branch(self) -> str:
        """Name of the currently checked-out branch."""
        return str(self._repo.active_branch)

    # ---- index / commit operations ----

    def add(self, paths: str | list[str]) -> None:
        """Stage *paths* for the next commit."""
        if isinstance(paths, str):
            paths = [paths]
        self._repo.index.add(paths)

    def commit(self, message: str) -> str:
        """Create a commit with *message*.

        Returns the hexsha of the new commit.
        """
        commit = self._repo.index.commit(message)
        return commit.hexsha

    @property
    def last_commit_message(self) -> str:
        """The message of the most recent commit on HEAD."""
        return self._repo.head.commit.message.strip()

    # ---- remote operations ----

    def push(self, remote: str = "origin", branch: str | None = None) -> None:
        """Push the current branch to *remote*."""
        refspec = branch or self.active_branch
        self._repo.remote(remote).push(refspec)

    def fetch(self, remote: str = "origin") -> None:
        """Fetch updates from *remote*."""
        self._repo.remote(remote).fetch()

    # ---- convenience ----

    @property
    def repo(self) -> git.Repo:
        """Access the underlying ``git.Repo`` if needed."""
        return self._repo

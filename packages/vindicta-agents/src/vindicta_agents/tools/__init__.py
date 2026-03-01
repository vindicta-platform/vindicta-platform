"""Tool infrastructure for the Vindicta Swarm.

Provides a ToolRegistry for agents to discover and invoke tools,
plus specialised tool modules for file I/O, Git, GitHub, and LLM ops.

Also re-exports git_tools helpers for backward compatibility.
"""

from __future__ import annotations

from typing import Any, Callable

# Re-export legacy git_tools for existing callers
from .git_tools import (
    run_cmd,
    verify_repo_clean,
    checkout_new_branch,
    commit_files,
    push_branch,
    create_pr,
    write_file,
)

__all__ = [
    "run_cmd",
    "verify_repo_clean",
    "checkout_new_branch",
    "commit_files",
    "push_branch",
    "create_pr",
    "write_file",
    "ToolNotFoundError",
    "ToolRegistry",
]


class ToolNotFoundError(Exception):
    """Raised when a tool name is not in the registry."""


class ToolRegistry:
    """Central registry mapping tool names to callables.

    Agents look up tools by name rather than importing modules directly,
    making it trivial to swap real implementations for test mocks.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        """Register *fn* under *name*."""
        self._tools[name] = fn

    def get(self, name: str) -> Callable[..., Any]:
        """Return the callable registered under *name*.

        Raises ``ToolNotFoundError`` if the name is unknown.
        """
        try:
            return self._tools[name]
        except KeyError:
            raise ToolNotFoundError(f"Tool not found: {name}") from None

    def list_tools(self) -> list[str]:
        """Return sorted list of all registered tool names."""
        return sorted(self._tools)

    def __contains__(self, name: str) -> bool:
        return name in self._tools

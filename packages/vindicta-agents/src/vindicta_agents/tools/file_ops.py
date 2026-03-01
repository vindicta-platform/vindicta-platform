"""File I/O tools — sandboxed to a workspace directory.

All paths are resolved relative to the workspace root. Any attempt to
escape the workspace (via ``..`` traversal or absolute paths outside
the root) raises ``SandboxViolationError``.
"""

from __future__ import annotations

from pathlib import Path


class SandboxViolationError(Exception):
    """Raised when a file operation escapes the workspace boundary."""


class FileOps:
    """Sandboxed file operations scoped to *workspace_root*."""

    def __init__(self, workspace_root: str | Path) -> None:
        self._root = Path(workspace_root).resolve()

    # ---- helpers ----

    def _resolve(self, relative: str | Path) -> Path:
        """Resolve *relative* against the workspace root.

        Raises ``SandboxViolationError`` if the resolved path escapes
        the workspace.
        """
        resolved = (self._root / relative).resolve()
        if not str(resolved).startswith(str(self._root)):
            raise SandboxViolationError(
                f"Path {relative!r} resolves outside workspace {self._root}"
            )
        return resolved

    # ---- public API ----

    def read_file(self, path: str | Path) -> str:
        """Read and return the text content of *path*."""
        return self._resolve(path).read_text(encoding="utf-8")

    def write_file(self, path: str | Path, content: str) -> Path:
        """Write *content* to *path*, creating parent dirs as needed.

        Returns the resolved path.
        """
        resolved = self._resolve(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")
        return resolved

    def list_directory(self, path: str | Path = ".") -> list[str]:
        """List the names of entries in *path*."""
        resolved = self._resolve(path)
        return sorted(entry.name for entry in resolved.iterdir())

    def create_directory(self, path: str | Path) -> Path:
        """Create *path* and any missing parents.

        Returns the resolved path.
        """
        resolved = self._resolve(path)
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved

    def exists(self, path: str | Path) -> bool:
        """Return ``True`` if *path* exists."""
        return self._resolve(path).exists()

    def is_directory(self, path: str | Path) -> bool:
        """Return ``True`` if *path* is a directory."""
        return self._resolve(path).is_dir()

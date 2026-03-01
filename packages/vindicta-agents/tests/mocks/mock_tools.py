"""Mock tool implementations for testing.

Provides in-memory substitutes for file, git, GitHub, and LLM tools
that can be injected via SwarmConfig during E2E and integration tests.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class MockFileOps:
    """In-memory file system for tests."""

    def __init__(self) -> None:
        self._files: Dict[str, str] = {}
        self._dirs: set[str] = {"."}

    def read_file(self, path: str) -> str:
        if path not in self._files:
            raise FileNotFoundError(path)
        return self._files[path]

    def write_file(self, path: str, content: str) -> str:
        self._files[path] = content
        return path

    def exists(self, path: str) -> bool:
        return path in self._files or path in self._dirs

    def list_directory(self, path: str = ".") -> List[str]:
        prefix = path.rstrip("/") + "/"
        entries = set()
        for p in self._files:
            if p.startswith(prefix):
                rel = p[len(prefix) :]
                entries.add(rel.split("/")[0])
        return sorted(entries)

    def create_directory(self, path: str) -> str:
        self._dirs.add(path)
        return path


class MockGitWorkspace:
    """Records git operations without executing them."""

    def __init__(self) -> None:
        self.branches: List[str] = ["main"]
        self.current_branch: str = "main"
        self.commits: List[Dict[str, Any]] = []
        self.pushed: bool = False

    def checkout(self, branch: str, create: bool = False) -> None:
        if create and branch not in self.branches:
            self.branches.append(branch)
        self.current_branch = branch

    def branch_exists(self, name: str) -> bool:
        return name in self.branches

    def add(self, paths: str | List[str] = ".") -> None:
        pass  # no-op

    def commit(self, message: str) -> str:
        sha = f"mock-{len(self.commits):04d}"
        self.commits.append(
            {"sha": sha, "message": message, "branch": self.current_branch}
        )
        return sha

    def push(self) -> None:
        self.pushed = True

    def fetch(self) -> None:
        pass


class MockGitHubClient:
    """Records GitHub API calls without making them."""

    def __init__(self) -> None:
        self.issues: List[Dict[str, Any]] = []
        self.prs: List[Dict[str, Any]] = []
        self.merged: List[str] = []

    def create_issue(self, title: str, body: str = "", **kwargs) -> Dict[str, Any]:
        issue = {
            "number": len(self.issues) + 1,
            "title": title,
            "body": body,
            "url": f"https://github.com/mock/issues/{len(self.issues) + 1}",
        }
        self.issues.append(issue)
        return issue

    def create_pr(
        self, title: str, body: str = "", head: str = "", base: str = "main"
    ) -> Any:
        class PRResult:
            def __init__(self, num, url_):
                self.number = num
                self.url = url_

        pr_num = len(self.prs) + 1
        pr = {
            "number": pr_num,
            "title": title,
            "head": head,
            "base": base,
            "url": f"https://github.com/mock/pull/{pr_num}",
        }
        self.prs.append(pr)
        return PRResult(pr_num, pr["url"])

    def merge_pr(self, pr_url: str) -> None:
        self.merged.append(pr_url)

    def list_issues(self) -> List[Dict[str, Any]]:
        return list(self.issues)


class MockLLMProvider:
    """Deterministic LLM for testing — returns controlled responses."""

    def __init__(
        self, text_response: str = "[MOCK]", json_response: Optional[List[Dict]] = None
    ) -> None:
        self._text = text_response
        self._json = json_response or [
            {
                "id": "task-1",
                "description": "Mock task",
                "target_realm": "vindicta-engine",
                "status": "pending",
            },
        ]

    def execute(self, system: Optional[str], prompt: str) -> str:
        return f"{self._text} | {prompt[:50]}"

    def execute_json(self, system: Optional[str], prompt: str) -> List[Dict]:
        return self._json

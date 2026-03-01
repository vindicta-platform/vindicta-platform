"""Unit tests for the Tool Infrastructure (Phase 1).

Tests cover:
- ToolRegistry (register, lookup, not-found)
- FileOps (read, write, list, mkdir, sandbox boundary)
- GitWorkspace (branch, stage, commit — mocked git.Repo)
- GitHubClient (create_issue, create_pr — mocked PyGithub)
- OllamaLLMProvider (generate_text, generate_json — mocked ollama)
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from vindicta_agents.tools import ToolNotFoundError, ToolRegistry
from vindicta_agents.tools.file_ops import FileOps, SandboxViolationError


# ──────────────────────────────────────────────
# ToolRegistry
# ──────────────────────────────────────────────


class TestToolRegistry:
    def test_register_and_get(self) -> None:
        reg = ToolRegistry()
        fn = lambda x: x  # noqa: E731
        reg.register("echo", fn)
        assert reg.get("echo") is fn

    def test_get_unknown_raises(self) -> None:
        reg = ToolRegistry()
        with pytest.raises(ToolNotFoundError):
            reg.get("nonexistent")

    def test_contains(self) -> None:
        reg = ToolRegistry()
        reg.register("a", lambda: None)
        assert "a" in reg
        assert "b" not in reg

    def test_list_tools(self) -> None:
        reg = ToolRegistry()
        reg.register("beta", lambda: None)
        reg.register("alpha", lambda: None)
        assert reg.list_tools() == ["alpha", "beta"]


# ──────────────────────────────────────────────
# FileOps
# ──────────────────────────────────────────────


class TestFileOps:
    def test_write_and_read(self, tmp_path: Path) -> None:
        ops = FileOps(tmp_path)
        ops.write_file("hello.txt", "world")
        assert ops.read_file("hello.txt") == "world"

    def test_write_creates_parents(self, tmp_path: Path) -> None:
        ops = FileOps(tmp_path)
        ops.write_file("a/b/c.txt", "nested")
        assert ops.read_file("a/b/c.txt") == "nested"

    def test_list_directory(self, tmp_path: Path) -> None:
        ops = FileOps(tmp_path)
        ops.write_file("x.txt", "")
        ops.write_file("y.txt", "")
        listing = ops.list_directory()
        assert "x.txt" in listing
        assert "y.txt" in listing

    def test_create_directory(self, tmp_path: Path) -> None:
        ops = FileOps(tmp_path)
        ops.create_directory("sub/deep")
        assert ops.is_directory("sub/deep")

    def test_sandbox_violation(self, tmp_path: Path) -> None:
        ops = FileOps(tmp_path)
        with pytest.raises(SandboxViolationError):
            ops.write_file("../../escape.txt", "bad")

    def test_exists(self, tmp_path: Path) -> None:
        ops = FileOps(tmp_path)
        assert not ops.exists("nope.txt")
        ops.write_file("nope.txt", "now exists")
        assert ops.exists("nope.txt")


# ──────────────────────────────────────────────
# GitWorkspace (mocked)
# ──────────────────────────────────────────────


class TestGitWorkspace:
    def test_checkout_creates_branch(self) -> None:
        from vindicta_agents.tools import git_ops

        with patch.object(git_ops, "git") as mock_git:
            ws = git_ops.GitWorkspace("/fake/repo")
            ws.checkout("feature/test", create=True)
            ws._repo.git.checkout.assert_called_once_with("-b", "feature/test")

    def test_checkout_existing_branch(self) -> None:
        from vindicta_agents.tools import git_ops

        with patch.object(git_ops, "git") as mock_git:
            ws = git_ops.GitWorkspace("/fake/repo")
            ws.checkout("main")
            ws._repo.git.checkout.assert_called_once_with("main")

    def test_branch_exists(self) -> None:
        from vindicta_agents.tools import git_ops

        with patch.object(git_ops, "git") as mock_git:
            mock_branch = MagicMock()
            mock_branch.name = "feature/existing"
            mock_git.Repo.return_value.branches = [mock_branch]

            ws = git_ops.GitWorkspace("/fake/repo")
            assert ws.branch_exists("feature/existing")
            assert not ws.branch_exists("feature/nope")

    def test_add_and_commit(self) -> None:
        from vindicta_agents.tools import git_ops

        with patch.object(git_ops, "git") as mock_git:
            mock_commit = MagicMock()
            mock_commit.hexsha = "abc123"
            mock_git.Repo.return_value.index.commit.return_value = mock_commit

            ws = git_ops.GitWorkspace("/fake/repo")
            ws.add(["file.py"])
            ws._repo.index.add.assert_called_once_with(["file.py"])

            sha = ws.commit("test commit")
            assert sha == "abc123"

    def test_add_single_string(self) -> None:
        from vindicta_agents.tools import git_ops

        with patch.object(git_ops, "git") as mock_git:
            ws = git_ops.GitWorkspace("/fake/repo")
            ws.add("single.py")
            ws._repo.index.add.assert_called_once_with(["single.py"])


# ──────────────────────────────────────────────
# GitHubClient (mocked)
# ──────────────────────────────────────────────


class TestGitHubClient:
    def test_create_issue(self) -> None:
        from vindicta_agents.tools import github_ops

        with patch.object(github_ops, "Github") as mock_gh_cls:
            mock_issue = MagicMock()
            mock_issue.number = 42
            mock_issue.title = "Test"
            mock_issue.html_url = "https://github.com/test/42"

            mock_repo = MagicMock()
            mock_repo.create_issue.return_value = mock_issue
            mock_gh_cls.return_value.get_repo.return_value = mock_repo

            client = github_ops.GitHubClient(token="fake-token")
            result = client.create_issue("owner/repo", "Test", "body")

            assert result.number == 42
            assert result.title == "Test"

    def test_create_pr(self) -> None:
        from vindicta_agents.tools import github_ops

        with patch.object(github_ops, "Github") as mock_gh_cls:
            mock_pr = MagicMock()
            mock_pr.number = 10
            mock_pr.title = "PR"
            mock_pr.html_url = "https://github.com/test/pull/10"

            mock_repo = MagicMock()
            mock_repo.create_pull.return_value = mock_pr
            mock_gh_cls.return_value.get_repo.return_value = mock_repo

            client = github_ops.GitHubClient(token="fake-token")
            result = client.create_pr("owner/repo", "PR", head="feature", base="main")

            assert result.number == 10


# ──────────────────────────────────────────────
# OllamaLLMProvider (mocked)
# ──────────────────────────────────────────────


class TestOllamaLLMProvider:
    def test_generate_text(self) -> None:
        from vindicta_agents.tools import llm_ops

        with patch.object(llm_ops, "_ollama_pkg") as mock_pkg:
            mock_pkg.Client.return_value.chat.return_value = {
                "message": {"content": "Hello!"}
            }

            provider = llm_ops.OllamaLLMProvider(model="test-model")
            result = provider.generate_text("Say hello", system="Be nice")

            assert result == "Hello!"
            mock_pkg.Client.return_value.chat.assert_called_once()

    def test_generate_json(self) -> None:
        from vindicta_agents.tools import llm_ops

        with patch.object(llm_ops, "_ollama_pkg") as mock_pkg:
            mock_pkg.Client.return_value.chat.return_value = {
                "message": {"content": '{"status": "ok"}'}
            }

            provider = llm_ops.OllamaLLMProvider(model="test-model")
            result = provider.generate_json("Return JSON")

            assert result == {"status": "ok"}

    def test_generate_json_strips_code_fences(self) -> None:
        from vindicta_agents.tools import llm_ops

        with patch.object(llm_ops, "_ollama_pkg") as mock_pkg:
            mock_pkg.Client.return_value.chat.return_value = {
                "message": {"content": '```json\n{"status": "ok"}\n```'}
            }

            provider = llm_ops.OllamaLLMProvider(model="test-model")
            result = provider.generate_json("Return JSON")

            assert result == {"status": "ok"}

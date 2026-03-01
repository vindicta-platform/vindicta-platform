"""GitHub API tools — thin wrapper around PyGithub.

Provides a ``GitHubClient`` class that wraps ``github.Github`` with
the subset of operations that agents need: issues, PRs, file contents.

Auth is via a single shared ``GITHUB_TOKEN`` environment variable.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from github import Github
from github.PullRequest import PullRequest as GHPullRequest
from github.Issue import Issue as GHIssue
from github.Repository import Repository as GHRepo


@dataclass(frozen=True)
class IssueResult:
    """Lightweight representation of a created/fetched issue."""

    number: int
    title: str
    url: str


@dataclass(frozen=True)
class PRResult:
    """Lightweight representation of a created PR."""

    number: int
    title: str
    url: str


class GitHubClient:
    """Simplified GitHub API client backed by PyGithub.

    Parameters
    ----------
    token:
        GitHub personal access token.  Defaults to the
        ``GITHUB_TOKEN`` environment variable.
    """

    def __init__(self, token: str | None = None) -> None:
        self._token = token or os.environ["GITHUB_TOKEN"]
        self._gh = Github(self._token)

    def _get_repo(self, repo_full_name: str) -> GHRepo:
        """Return a ``Repository`` object for *repo_full_name* (``owner/repo``)."""
        return self._gh.get_repo(repo_full_name)

    # ---- issues ----

    def create_issue(
        self,
        repo: str,
        title: str,
        body: str = "",
        labels: list[str] | None = None,
    ) -> IssueResult:
        """Create an issue in *repo*.

        Returns an ``IssueResult`` with number, title, and URL.
        """
        gh_repo = self._get_repo(repo)
        issue: GHIssue = gh_repo.create_issue(
            title=title,
            body=body,
            labels=labels or [],
        )
        return IssueResult(
            number=issue.number,
            title=issue.title,
            url=issue.html_url,
        )

    def list_issues(
        self,
        repo: str,
        labels: list[str] | None = None,
        state: str = "open",
    ) -> list[IssueResult]:
        """List issues in *repo*, optionally filtered by *labels*."""
        gh_repo = self._get_repo(repo)
        issues = gh_repo.get_issues(
            state=state,
            labels=[gh_repo.get_label(lbl) for lbl in labels] if labels else [],
        )
        return [
            IssueResult(number=i.number, title=i.title, url=i.html_url) for i in issues
        ]

    # ---- pull requests ----

    def create_pr(
        self,
        repo: str,
        title: str,
        body: str = "",
        head: str = "",
        base: str = "main",
    ) -> PRResult:
        """Create a pull request in *repo*.

        Returns a ``PRResult`` with number, title, and URL.
        """
        gh_repo = self._get_repo(repo)
        pr: GHPullRequest = gh_repo.create_pull(
            title=title,
            body=body,
            head=head,
            base=base,
        )
        return PRResult(
            number=pr.number,
            title=pr.title,
            url=pr.html_url,
        )

    def merge_pr(
        self,
        repo: str,
        pr_number: int,
        merge_method: str = "squash",
    ) -> None:
        """Merge pull request *pr_number* in *repo*."""
        gh_repo = self._get_repo(repo)
        pr = gh_repo.get_pull(pr_number)
        pr.merge(merge_method=merge_method)

    # ---- file contents ----

    def get_file_contents(
        self,
        repo: str,
        path: str,
        ref: str = "main",
    ) -> str:
        """Return the decoded text content of *path* in *repo*."""
        gh_repo = self._get_repo(repo)
        content = gh_repo.get_contents(path, ref=ref)
        if isinstance(content, list):
            raise ValueError(f"Path {path!r} is a directory, not a file")
        return content.decoded_content.decode("utf-8")

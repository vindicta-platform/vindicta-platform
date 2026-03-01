"""Swarm Configuration & Dependency Injection.

Defines the configurable dependencies injected into LangGraph nodes
via ``RunnableConfig["configurable"]``.

Usage::

    vindicta_swarm.invoke(state, config={"configurable": {
        "llm_provider": OllamaLLMProvider(),
        "tools": tool_registry,
        "github_client": GitHubClient(),
        "supervisor": my_supervisor,
    }})
"""

from __future__ import annotations

import json
import os
import urllib.request
import uuid
from typing import Any, Protocol, TypedDict, runtime_checkable

from ..utils.logger import logger
from ..tools import git_tools


@runtime_checkable
class LLMProvider(Protocol):
    def execute(self, system: str | None, prompt: str) -> str: ...
    def execute_json(self, system: str | None, prompt: str) -> list[dict]: ...


class SwarmConfig(TypedDict, total=False):
    """Configurable dependencies passed via RunnableConfig["configurable"]."""

    llm_provider: Any  # LLMProvider protocol (Ollama or Mock)
    supervisor: Any  # AxiomaticSupervisor instance
    nexus_client: Any  # Optional NexusClient for reporting
    tools: Any  # ToolRegistry instance
    github_client: Any  # GitHubClient instance
    github_token: str  # Shared GITHUB_TOKEN (fallback for GitHubClient)
    workspace_root: str  # Absolute path to the workspace for file/git ops
    domain_map: dict[str, str]


class MockLLMProvider:
    def execute(self, system: str | None, prompt: str) -> str:
        return "[MOCKED EXECUTION] This is a placeholder response."

    def execute_json(self, system: str | None, prompt: str) -> list[dict]:
        return [{"id": "mock-task-1", "description": "Mock Task", "status": "pending"}]


class OllamaLLMProvider:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.model = model
        self.base_url = base_url

    def execute(self, system: str | None, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "")
        except Exception as e:
            return f"[Ollama Error] {str(e)}"

    def execute_json(self, system: str | None, prompt: str) -> list[dict]:
        """Execute and parse JSON from the response, stripping markdown fences."""
        response = self.execute(system, prompt + "\nRespond ONLY with valid JSON.")
        try:
            clean = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except (json.JSONDecodeError, ValueError):
            return []


class ShowcaseProvider:
    """
    Deterministic provider for the 'Swarm Showcase' demo.
    Ensures 100% success rate for the 'Add Health Check' scenario.
    """

    def __init__(self):
        self.branch_name = f"feat/health-check-{uuid.uuid4().hex[:8]}"

    def execute(self, system: str | None, prompt: str) -> str:
        # Product Owner
        if "Product Owner" in (system or ""):
            return (
                "# Functional Specification: Standardized Health Check\n\n"
                "To improve observability, all domains must expose a standardized health check endpoint.\n"
                "**Requirement**: Add a file that indicates service health and realm identity.\n"
            )

        # Architect
        if "Architect" in (system or ""):
            return (
                "# Implementation Plan\n\n"
                "We will implement a simple check mechanism appropriate for each tech stack.\n"
                "- Python: `src/<package>/health.py` with `check_health()` function.\n"
                "- Node: `src/health.js` exporting `checkHealth()` function.\n"
            )

        return "I accept this task."

    def execute_json(self, system: str | None, prompt: str) -> list[dict]:
        # ADL - Validates prompt to ensure we are in the right context
        return [
            {
                "id": "1",
                "description": "Implement health check",
                "target_realm": "vindicta-engine",
                "status": "pending",
            },
            {
                "id": "2",
                "description": "Implement health check",
                "target_realm": "warscribe-system",
                "status": "pending",
            },
            {
                "id": "3",
                "description": "Implement health check",
                "target_realm": "vindicta-economy",
                "status": "pending",
            },
            {
                "id": "4",
                "description": "Implement health check",
                "target_realm": "primordia-ai",
                "status": "pending",
            },
            {
                "id": "5",
                "description": "Implement health check",
                "target_realm": "meta-oracle",
                "status": "pending",
            },
            {
                "id": "6",
                "description": "Implement health check",
                "target_realm": "logi-slate-ui",
                "status": "pending",
            },
            {
                "id": "7",
                "description": "Implement health check",
                "target_realm": "vindicta-portal",
                "status": "pending",
            },
            {
                "id": "8",
                "description": "Implement health check",
                "target_realm": "vindicta-api",
                "status": "pending",
            },
        ]

    def execute_domain_task(self, realm: str, repo_path: str) -> str:
        """
        Executes the actual git operations for the given realm.
        """
        logger.info(f"ShowcaseExecutor: Processing {realm} in {repo_path}")

        try:
            # 1. Checkout Branch
            git_tools.checkout_new_branch(repo_path, self.branch_name)

            # 2. Add Code
            self._write_health_code(realm, repo_path)

            # 3. Commit
            git_tools.commit_files(
                repo_path,
                "feat: add standardized health check endpoint",
                author_email="260104759+vindicta-bot@users.noreply.github.com",
            )

            # 4. Push
            git_tools.push_branch(repo_path, self.branch_name)

            # 5. Create PR
            pr_url = git_tools.create_pr(
                repo_path,
                title="feat: Standardized Health Check",
                body=f"Automated PR by Vindicta Swarm.\n\nAdds health check for realm: `{realm}`.",
                reviewer="brandon-fox",
            )

            return f"PR Created: {pr_url}"

        except Exception as e:
            logger.error("showcase_execution_failed", realm=realm, error=str(e))
            return f"Failed: {str(e)}"

    def _write_health_code(self, realm: str, repo_path: str):
        is_node = os.path.exists(os.path.join(repo_path, "package.json"))

        if is_node:
            content = (
                "/**\n * Health Check Module\n */\n"
                "export function checkHealth() {\n"
                f"  return {{ status: 'ok', realm: '{realm}', timestamp: Date.now() }};\n"
                "}\n"
            )
            git_tools.write_file(repo_path, "src/health.js", content)
        else:
            pkg_name = realm.replace("-", "_").lower()
            if realm == "Primordia-AI":
                pkg_name = "primordia"
            if realm == "Meta-Oracle":
                pkg_name = "meta_oracle"

            target_file = f"src/{pkg_name}/health.py"

            if not os.path.exists(os.path.join(repo_path, "src")):
                target_file = "health.py"

            content = (
                "import time\n\n"
                "def check_health() -> dict:\n"
                '    """Returns the health status of the service."""\n'
                f"    return {{'status': 'ok', 'realm': '{realm}', 'timestamp': time.time()}}\n"
            )
            git_tools.write_file(repo_path, target_file, content)

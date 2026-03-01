"""Unit tests for Phase 3: Agent Node Upgrades.

Tests cover:
- PO node (spec generation, decline memory integration)
- Architect node (plan from spec)
- ADL node (task slicing)
- SD node (delegation)
- Domain agents (code generation)
- SD Review (approve/reject)
- SSE node (PR creation)
- SM / SM_Merge nodes (boot / merge)
- Graph topology (nexus wiring)
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from vindicta_agents.swarm.config import MockLLMProvider
from vindicta_agents.swarm.meta_graph import (
    adl_node,
    architect_node,
    product_owner_node,
)
from vindicta_agents.swarm.domain_graph import (
    sd_node,
    sd_review_node,
    sse_node,
    sm_node,
    sm_merge_node,
    tech_priest_node,
    logos_historian_node,
    void_banker_node,
    task_router,
)
from vindicta_agents.swarm.prompts import REALM_TO_AGENT, REALM_TO_SYSTEM_PROMPT
from vindicta_agents.swarm.spec_queue import DeclineRecord


# ── Fixtures ─────────────────────────────────────────────────────────


@pytest.fixture
def mock_config():
    """Config with MockLLMProvider."""
    return {"configurable": {"llm_provider": MockLLMProvider()}}


@pytest.fixture
def base_state():
    """Minimal valid state."""
    return {
        "intent": "Add health check endpoint",
        "sdd_stage": "",
        "feature_name": "",
        "branch_name": "",
        "spec_dir": "",
        "spec_content": None,
        "plan_content": None,
        "tasks_content": None,
        "tasks": [],
        "pr_url": None,
        "issue_urls": [],
        "spec_queue": [],
        "decline_memory": [],
        "current_phase": "",
        "error_log": None,
        "execution_log": [],
    }


# ── PO Node ──────────────────────────────────────────────────────────


class TestProductOwnerNode:
    def test_generates_spec(self, base_state, mock_config):
        result = product_owner_node(base_state, mock_config)
        assert result["spec_content"] is not None
        assert result["sdd_stage"] == "specify"
        assert "PO: generated spec" in result["execution_log"][0]

    def test_uses_decline_memory(self, base_state, mock_config):
        base_state["decline_memory"] = [
            DeclineRecord(feature_name="bad", reason="Too vague"),
        ]
        result = product_owner_node(base_state, mock_config)
        # The mock just returns the prompt back, which should include decline context
        assert result["spec_content"] is not None


# ── Architect Node ───────────────────────────────────────────────────


class TestArchitectNode:
    def test_creates_plan(self, base_state, mock_config):
        base_state["spec_content"] = "A spec about health checks"
        result = architect_node(base_state, mock_config)
        assert result["plan_content"] is not None
        assert result["sdd_stage"] == "plan"
        assert "Architect: plan created" in result["execution_log"]


# ── ADL Node ─────────────────────────────────────────────────────────


class TestADLNode:
    def test_generates_tasks(self, base_state, mock_config):
        base_state["plan_content"] = "A plan with three components"
        result = adl_node(base_state, mock_config)
        assert len(result["tasks"]) > 0
        assert result["sdd_stage"] == "tasks"
        assert result["current_phase"] == "review"


# ── SD Node ──────────────────────────────────────────────────────────


class TestSDNode:
    def test_delegates(self, base_state, mock_config):
        base_state["tasks"] = [
            {
                "id": "t1",
                "description": "task",
                "target_realm": "vindicta-engine",
                "status": "pending",
            },
        ]
        result = sd_node(base_state, mock_config)
        assert result["sdd_stage"] == "implement"
        assert "SD: delegated" in result["execution_log"][0]


# ── Domain Agents ────────────────────────────────────────────────────


class TestDomainAgents:
    def test_tech_priest(self, base_state, mock_config):
        base_state["tasks"] = [
            {
                "id": "t1",
                "description": "engine task",
                "target_realm": "vindicta-engine",
                "status": "pending",
            },
        ]
        result = tech_priest_node(base_state, mock_config)
        assert any("TechPriest" in e for e in result["execution_log"])

    def test_logos_historian(self, base_state, mock_config):
        base_state["tasks"] = [
            {
                "id": "t1",
                "description": "warscribe task",
                "target_realm": "warscribe-system",
                "status": "pending",
            },
        ]
        result = logos_historian_node(base_state, mock_config)
        assert any("LogosHistorian" in e for e in result["execution_log"])

    def test_void_banker(self, base_state, mock_config):
        base_state["tasks"] = [
            {
                "id": "t1",
                "description": "economy task",
                "target_realm": "vindicta-economy",
                "status": "pending",
            },
        ]
        result = void_banker_node(base_state, mock_config)
        assert any("VoidBanker" in e for e in result["execution_log"])

    def test_no_matching_tasks(self, base_state, mock_config):
        base_state["tasks"] = [
            {
                "id": "t1",
                "description": "other",
                "target_realm": "other-realm",
                "status": "pending",
            },
        ]
        result = tech_priest_node(base_state, mock_config)
        assert "TechPriest activated" in result["execution_log"]


# ── SD Review ────────────────────────────────────────────────────────


class TestSDReviewNode:
    def test_review(self, base_state, mock_config):
        base_state["tasks"] = [
            {"id": "t1", "code_diff": "def foo(): pass", "status": "completed"},
        ]
        result = sd_review_node(base_state, mock_config)
        assert result["sdd_stage"] == "verify"
        assert any("SD_Review" in e for e in result["execution_log"])


# ── SSE Node ─────────────────────────────────────────────────────────


class TestSSENode:
    def test_review_no_github(self, base_state, mock_config):
        """SSE runs review but no PR without github_client."""
        base_state["tasks"] = [
            {"id": "t1", "code_diff": "def bar(): pass", "status": "completed"},
        ]
        result = sse_node(base_state, mock_config)
        assert result["pr_url"] is None
        assert any("SSE" in e for e in result["execution_log"])

    def test_pr_creation_with_github(self, base_state):
        mock_pr = MagicMock()
        mock_pr.url = "https://github.com/test/pr/1"
        mock_gh = MagicMock()
        mock_gh.create_pr.return_value = mock_pr

        # Use a provider that returns APPROVE in its output
        class ApproveProvider:
            def execute(self, system, prompt):
                return "APPROVE all changes look good"

            def execute_json(self, system, prompt):
                return []

        config = {
            "configurable": {
                "llm_provider": ApproveProvider(),
                "github_client": mock_gh,
            }
        }
        base_state["tasks"] = [{"id": "t1", "code_diff": "code", "status": "completed"}]
        base_state["feature_name"] = "health-check"
        base_state["branch_name"] = "feat/health-check"

        result = sse_node(base_state, config)
        assert result["pr_url"] == "https://github.com/test/pr/1"
        mock_gh.create_pr.assert_called_once()


# ── SM Nodes ─────────────────────────────────────────────────────────


class TestSMNodes:
    def test_sm_boot(self, base_state, mock_config):
        result = sm_node(base_state, mock_config)
        assert result["sdd_stage"] == "specify"
        assert "SM: swarm booted" in result["execution_log"][0]

    def test_sm_merge(self, base_state, mock_config):
        base_state["pr_url"] = "https://github.com/test/pr/1"
        result = sm_merge_node(base_state, mock_config)
        assert result["sdd_stage"] == "done"
        assert "SM: PR merged" in result["execution_log"][0]


# ── Task Router ──────────────────────────────────────────────────────


class TestTaskRouter:
    def test_routes_to_agents(self, base_state):
        base_state["tasks"] = [
            {"id": "t1", "target_realm": "vindicta-engine", "status": "pending"},
            {"id": "t2", "target_realm": "warscribe-system", "status": "pending"},
        ]
        result = task_router(base_state)
        assert "TechPriest" in result
        assert "LogosHistorian" in result

    def test_no_pending_routes_to_end(self, base_state):
        from langgraph.graph import END

        base_state["tasks"] = [
            {"id": "t1", "target_realm": "vindicta-engine", "status": "completed"},
        ]
        assert task_router(base_state) == END


# ── Prompts Module ───────────────────────────────────────────────────


class TestPrompts:
    def test_realm_mapping(self):
        assert REALM_TO_AGENT["vindicta-engine"] == "TechPriest"
        assert REALM_TO_AGENT["warscribe-system"] == "LogosHistorian"
        assert REALM_TO_AGENT["vindicta-economy"] == "VoidBanker"

    def test_realm_prompts(self):
        for realm in REALM_TO_AGENT:
            assert realm in REALM_TO_SYSTEM_PROMPT

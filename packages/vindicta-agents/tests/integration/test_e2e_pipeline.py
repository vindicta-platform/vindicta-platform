"""End-to-end integration test for the autonomous SDD pipeline.

Runs the full pipeline (SM → PO → Architect → ADL → SD → Domain →
SD_Review → SSE → SM_Merge) with mock tools, verifying state
transitions at each stage.
"""

from __future__ import annotations

import pytest

from vindicta_agents.swarm.config import MockLLMProvider
from vindicta_agents.swarm.domain_graph import (
    sd_node,
    sd_review_node,
    sm_merge_node,
    sm_node,
    sse_node,
    tech_priest_node,
)
from vindicta_agents.swarm.meta_graph import (
    adl_node,
    architect_node,
    product_owner_node,
)
from vindicta_agents.swarm.review_gates import (
    AutoDeclineBackend,
    ReviewGate,
)
from vindicta_agents.swarm.spec_queue import DeclineMemory, SpecQueue

from tests.mocks.mock_tools import (
    MockFileOps,
    MockGitHubClient,
    MockGitWorkspace,
)

# Import the configurable mock separately to avoid name clash
from tests.mocks.mock_tools import MockLLMProvider as TestMockProvider

# LangGraph's operator.add annotation only works inside the graph runtime.
# Outside, dict.update() replaces list values.  This helper manually extends them.
_LIST_FIELDS = {"execution_log", "issue_urls", "tasks"}


def merge_state(state: dict, delta: dict) -> None:
    """Merge node result into state, extending list fields instead of replacing."""
    for key, value in delta.items():
        if key in _LIST_FIELDS and isinstance(value, list):
            state.setdefault(key, []).extend(value)
        else:
            state[key] = value


@pytest.fixture
def mock_config():
    return {"configurable": {"llm_provider": MockLLMProvider()}}


@pytest.fixture
def initial_state():
    return {
        "intent": "Add health check endpoint to vindicta-engine",
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


class TestE2EHappyPath:
    """Full pipeline with all approval gates auto-approved."""

    def test_full_pipeline(self, initial_state, mock_config):
        state = initial_state

        # 1. SM Boot
        merge_state(state, sm_node(state, mock_config))
        assert state["sdd_stage"] == "specify"

        # 2. PO generates spec
        merge_state(state, product_owner_node(state, mock_config))
        assert state["spec_content"] is not None
        assert state["sdd_stage"] == "specify"

        # 3. Architect creates plan
        merge_state(state, architect_node(state, mock_config))
        assert state["plan_content"] is not None
        assert state["sdd_stage"] == "plan"

        # 4. ADL generates tasks
        merge_state(state, adl_node(state, mock_config))
        assert len(state["tasks"]) > 0
        assert state["sdd_stage"] == "tasks"

        # 5. SD delegates
        merge_state(state, sd_node(state, mock_config))
        assert state["sdd_stage"] == "implement"

        # 6. Domain agent (TechPriest for vindicta-engine tasks)
        merge_state(state, tech_priest_node(state, mock_config))

        # 7. SD Review
        merge_state(state, sd_review_node(state, mock_config))
        assert state["sdd_stage"] == "verify"

        # 8. SSE (no GitHub client → no PR created)
        merge_state(state, sse_node(state, mock_config))

        # 9. SM Merge
        merge_state(state, sm_merge_node(state, mock_config))
        assert state["sdd_stage"] == "done"
        assert state["current_phase"] == "done"

        # Verify execution log accumulated from all stages
        log = state["execution_log"]
        assert any("SM: swarm booted" in e for e in log)
        assert any("PO: generated spec" in e for e in log)
        assert any("Architect: plan created" in e for e in log)
        assert any("SD: delegated" in e for e in log)
        assert any("SM:" in e and ("merged" in e or "merge" in e) for e in log)

    def test_pipeline_with_github(self, initial_state):
        """Full pipeline with mock GitHub client — verifies PR creation."""
        mock_gh = MockGitHubClient()

        class ApproveProvider:
            def execute(self, system, prompt):
                return "APPROVE all looks good"

            def execute_json(self, system, prompt):
                return [
                    {
                        "id": "t-1",
                        "description": "task",
                        "target_realm": "vindicta-engine",
                        "status": "pending",
                    }
                ]

        config = {
            "configurable": {
                "llm_provider": ApproveProvider(),
                "github_client": mock_gh,
            }
        }
        state = initial_state

        for node_fn in [
            sm_node,
            product_owner_node,
            architect_node,
            adl_node,
            sd_node,
            tech_priest_node,
            sd_review_node,
            sse_node,
            sm_merge_node,
        ]:
            merge_state(state, node_fn(state, config))

        assert state["pr_url"] is not None
        assert "github.com/mock/pull" in state["pr_url"]
        assert state["sdd_stage"] == "done"


class TestE2EDeclineFlow:
    """Pipeline where spec is declined and decline memory is populated."""

    def test_decline_stores_memory(self, initial_state, mock_config):
        import asyncio

        state = initial_state

        # SM + PO
        state.update(sm_node(state, mock_config))
        state.update(product_owner_node(state, mock_config))

        # Human declines
        gate = ReviewGate(
            backend=AutoDeclineBackend("Missing acceptance criteria"),
            gate_type="spec_review",
        )
        decision = asyncio.get_event_loop().run_until_complete(
            gate.review("Spec Review", state.get("spec_content", ""))
        )
        assert not decision.approved

        # Store in decline memory
        memory = DeclineMemory()
        memory.add(state.get("feature_name", ""), decision.reason)

        assert memory.count == 1
        assert "Missing acceptance criteria" in memory.format_for_prompt()


class TestMockTools:
    """Verify mock tool implementations work correctly."""

    def test_mock_file_ops(self):
        fs = MockFileOps()
        fs.write_file("src/main.py", "print('hello')")
        assert fs.exists("src/main.py")
        assert fs.read_file("src/main.py") == "print('hello')"

    def test_mock_git(self):
        git = MockGitWorkspace()
        git.checkout("feat/test", create=True)
        assert git.current_branch == "feat/test"
        sha = git.commit("test commit")
        assert sha.startswith("mock-")
        git.push()
        assert git.pushed

    def test_mock_github(self):
        gh = MockGitHubClient()
        issue = gh.create_issue("Test issue")
        assert issue["number"] == 1
        pr = gh.create_pr("Test PR", head="feat/test")
        assert pr.number == 1
        gh.merge_pr(pr.url)
        assert pr.url in gh.merged

    def test_mock_llm(self):
        llm = TestMockProvider(text_response="APPROVE")
        assert "APPROVE" in llm.execute(None, "test prompt")
        tasks = llm.execute_json(None, "tasks")
        assert len(tasks) == 1


class TestSpecQueue:
    """Queue-level integration."""

    def test_queue_fills_and_drains(self):
        q = SpecQueue(target_size=3)
        q.add("feat-1", "Spec 1")
        q.add("feat-2", "Spec 2")
        q.add("feat-3", "Spec 3")
        assert q.is_full

        item = q.pop()
        assert item.feature_name == "feat-1"
        assert not q.is_full
        assert q.slots_available == 1

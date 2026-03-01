from vindicta_agents.swarm.meta_graph import (
    product_owner_node,
    architect_node,
    adl_node,
)
from vindicta_agents.swarm.domain_graph import (
    tech_priest_node,
    logos_historian_node,
    void_banker_node,
    setup_execution_node,
    task_router,
)
from langgraph.graph import END


# --- Helper: default config ---
DEFAULT_CONFIG = {"configurable": {}}


# --- Meta-Graph Node Tests ---
class TestMetaGraphNodes:
    def test_product_owner_node(self):
        state = {"intent": "Test Intent"}
        result = product_owner_node(state, DEFAULT_CONFIG)
        assert result["current_phase"] == "planning"
        assert "spec_content" in result
        assert "[MOCKED EXECUTION]" in result["spec_content"]

    def test_architect_node(self):
        state = {"spec_content": "Test Spec"}
        result = architect_node(state, DEFAULT_CONFIG)
        assert "plan_content" in result
        assert "[MOCKED EXECUTION]" in result["plan_content"]

    def test_adl_node(self):
        state = {"plan_content": "Test Plan"}
        result = adl_node(state, DEFAULT_CONFIG)
        assert result["current_phase"] == "review"
        assert "tasks" in result
        assert len(result["tasks"]) >= 1

    def test_custom_provider_injected(self):
        class StubProvider:
            def execute(self, system, prompt):
                return "STUB_RESPONSE"

            def execute_json(self, system, prompt):
                return []

        config = {"configurable": {"llm_provider": StubProvider()}}
        result = product_owner_node({"intent": "test"}, config)
        assert result["spec_content"] == "STUB_RESPONSE"


# --- Domain-Graph Node Tests ---
class TestDomainGraphNodes:
    def test_setup_execution_node(self):
        result = setup_execution_node({"tasks": []})
        assert result["current_phase"] == "execution"

    def test_tech_priest_activation(self):
        result = tech_priest_node({"tasks": []}, DEFAULT_CONFIG)
        assert "TechPriest activated" in result["execution_log"]

    def test_logos_historian_activation(self):
        result = logos_historian_node({"tasks": []}, DEFAULT_CONFIG)
        assert "LogosHistorian activated" in result["execution_log"]

    def test_void_banker_activation(self):
        result = void_banker_node({"tasks": []}, DEFAULT_CONFIG)
        assert "VoidBanker activated" in result["execution_log"]

    def test_domain_node_with_supervisor(self):
        """Verify supervisor is called when injected."""

        class MockSupervisor:
            def __init__(self):
                self.calls = []

            def verify_state_transition(self, trace_id, delta):
                self.calls.append((trace_id, delta))

        supervisor = MockSupervisor()
        config = {"configurable": {"supervisor": supervisor}}

        tech_priest_node({"tasks": []}, config)
        assert len(supervisor.calls) == 1
        assert supervisor.calls[0][1] == {"execution_log": ["TechPriest activated"]}

    def test_domain_node_without_supervisor(self):
        """Verify nodes work fine without a supervisor (no crash)."""
        result = tech_priest_node({"tasks": []}, DEFAULT_CONFIG)
        assert "TechPriest activated" in result["execution_log"]


# --- Router Tests ---
class TestTaskRouter:
    def test_routes_to_tech_priest(self):
        state = {
            "tasks": [
                {
                    "id": "1",
                    "description": "x",
                    "target_realm": "vindicta-engine",
                    "status": "pending",
                }
            ]
        }
        result = task_router(state)
        assert result == ["TechPriest"]

    def test_routes_to_multiple_nodes(self):
        state = {
            "tasks": [
                {
                    "id": "1",
                    "description": "x",
                    "target_realm": "vindicta-engine",
                    "status": "pending",
                },
                {
                    "id": "2",
                    "description": "y",
                    "target_realm": "warscribe-system",
                    "status": "pending",
                },
            ]
        }
        result = task_router(state)
        assert "TechPriest" in result
        assert "LogosHistorian" in result

    def test_no_pending_tasks_returns_end(self):
        state = {
            "tasks": [
                {
                    "id": "1",
                    "description": "x",
                    "target_realm": "vindicta-engine",
                    "status": "completed",
                }
            ]
        }
        result = task_router(state)
        assert result == END

    def test_empty_tasks_returns_end(self):
        result = task_router({"tasks": []})
        assert result == END

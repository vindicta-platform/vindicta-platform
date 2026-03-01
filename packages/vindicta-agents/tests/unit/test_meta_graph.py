"""Unit tests for the refactored meta_graph module."""

import sys
import unittest

sys.path.insert(0, "src")

from vindicta_agents.swarm.meta_graph import (
    PLANNING_AGENTS,
    build_meta_graph,
    make_planning_node,
)
from vindicta_agents.swarm.config import MockLLMProvider


class TestMetaGraphStructure(unittest.TestCase):
    """Verify the compiled graph contains all expected nodes and edges."""

    def test_graph_has_all_planning_nodes(self):
        graph = build_meta_graph()
        nodes = graph.get_graph().nodes
        for agent_id in PLANNING_AGENTS:
            self.assertIn(agent_id, nodes, f"Node {agent_id} missing from meta graph")

    def test_graph_has_linear_flow(self):
        """PO -> Architect -> ADL -> END."""
        graph = build_meta_graph()
        g = graph.get_graph()
        # Each node should have exactly one outgoing edge (linear chain)
        edges_from = {}
        for edge in g.edges:
            src = edge.source
            edges_from.setdefault(src, []).append(edge.target)
        self.assertIn("Architect", edges_from.get("PO", []))
        self.assertIn("ADL", edges_from.get("Architect", []))


class TestMakePlanningNode(unittest.TestCase):
    """Verify the planning node factory produces correct behaviour."""

    def test_po_node_returns_spec(self):
        node_fn = make_planning_node("PO")
        state = {"intent": "Build a combat simulator"}
        config = {"configurable": {"llm_provider": MockLLMProvider()}}
        result = node_fn(state, config)
        self.assertIn("spec_content", result)
        self.assertIn("current_phase", result)
        self.assertEqual(result["current_phase"], "planning")

    def test_architect_node_returns_plan(self):
        node_fn = make_planning_node("Architect")
        state = {"spec_content": "Some spec text"}
        config = {"configurable": {"llm_provider": MockLLMProvider()}}
        result = node_fn(state, config)
        self.assertIn("plan_content", result)
        self.assertNotIn("current_phase", result)  # Architect has no phase_update

    def test_adl_node_returns_tasks_list(self):
        node_fn = make_planning_node("ADL")
        state = {"plan_content": "Some plan text"}
        config = {"configurable": {"llm_provider": MockLLMProvider()}}
        result = node_fn(state, config)
        self.assertIn("tasks", result)
        self.assertIsInstance(result["tasks"], list)
        self.assertEqual(result["current_phase"], "review")

    def test_unknown_agent_raises(self):
        with self.assertRaises(ValueError):
            make_planning_node("UnknownAgent")

    def test_node_function_name(self):
        node_fn = make_planning_node("PO")
        self.assertEqual(node_fn.__name__, "po_node")


if __name__ == "__main__":
    unittest.main()

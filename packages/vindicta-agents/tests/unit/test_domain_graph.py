import sys
import unittest

# Adjust path to import src
sys.path.append("src")

from vindicta_agents.swarm.domain_graph import build_domain_graph, DOMAIN_REGISTRY


class TestDomainGraphStructure(unittest.TestCase):
    def test_graph_construction(self):
        """Verify that the graph is built with all registered domain nodes."""
        graph = build_domain_graph()

        # Access the underlying graph to check nodes
        compiled_graph = graph.get_graph()
        nodes = compiled_graph.nodes

        # Check standard nodes
        self.assertIn("SetupExecution", nodes)

        # Check all registered domain nodes
        for realm, info in DOMAIN_REGISTRY.items():
            node_name = info["node_name"]
            self.assertIn(
                node_name,
                nodes,
                f"Node {node_name} for realm {realm} not found in graph",
            )

        print(f"Verified {len(DOMAIN_REGISTRY)} domain nodes + SetupExecution.")


if __name__ == "__main__":
    unittest.main()

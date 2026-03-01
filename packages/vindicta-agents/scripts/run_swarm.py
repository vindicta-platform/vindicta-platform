"""CLI entry point for the autonomous swarm.

Usage::

    uv run python -m scripts.run_swarm "Add health check endpoint"
    uv run python -m scripts.run_swarm --mock "Add health check endpoint"

Bootstraps the swarm with configured tools and LLM provider,
then executes the full SDD lifecycle.
"""

from __future__ import annotations

import argparse

from vindicta_agents.swarm.config import MockLLMProvider
from vindicta_agents.swarm.meta_graph import (
    product_owner_node,
    architect_node,
    adl_node,
)
from vindicta_agents.swarm.domain_graph import (
    sd_node,
    sm_node,
    sm_merge_node,
    sd_review_node,
    sse_node,
)


def build_initial_state(intent: str) -> dict:
    """Create a fresh VindictaState dict."""
    return {
        "intent": intent,
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


def run_pipeline(intent: str, use_mock: bool = True) -> dict:
    """Execute the full SDD pipeline sequentially.

    Parameters
    ----------
    intent:
        Feature description to implement.
    use_mock:
        If True, use MockLLMProvider. If False, attempt Ollama.

    Returns
    -------
    dict
        Final state after pipeline completion.
    """
    if use_mock:
        provider = MockLLMProvider()
    else:
        try:
            from vindicta_agents.tools.llm_ops import OllamaLLMProvider

            class OllamaAdapter:
                """Adapt OllamaLLMProvider to LLMProvider protocol."""

                def __init__(self):
                    self._inner = OllamaLLMProvider()

                def execute(self, system, prompt):
                    return self._inner.generate_text(system=system or "", prompt=prompt)

                def execute_json(self, system, prompt):
                    return self._inner.generate_json(system=system or "", prompt=prompt)

            provider = OllamaAdapter()
        except Exception as e:
            print(f"⚠️  Ollama unavailable ({e}), falling back to mock")
            provider = OllamaAdapter() if False else MockLLMProvider()

    config = {"configurable": {"llm_provider": provider}}
    state = build_initial_state(intent)

    # Pipeline stages
    stages = [
        ("SM Boot", sm_node),
        ("PO: Spec Generation", product_owner_node),
        ("Architect: Plan Creation", architect_node),
        ("ADL: Task Slicing", adl_node),
        ("SD: Delegation", sd_node),
        ("SD Review", sd_review_node),
        ("SSE: Final Review", sse_node),
        ("SM: Merge", sm_merge_node),
    ]

    for name, node_fn in stages:
        print(f"\n{'=' * 60}")
        print(f"  ▶ {name}")
        print(f"{'=' * 60}")

        result = node_fn(state, config)
        state.update(result)

        # Print execution log entries
        for entry in result.get("execution_log", []):
            print(f"    📋 {entry}")

        if state.get("error_log"):
            print(f"    ❌ Error: {state['error_log']}")
            break

    print(f"\n{'=' * 60}")
    print("  🏁 Pipeline Complete")
    print(f"{'=' * 60}")
    print(f"  SDD Stage: {state.get('sdd_stage', '?')}")
    print(f"  Phase: {state.get('current_phase', '?')}")
    print(f"  Tasks: {len(state.get('tasks', []))}")
    print(f"  PR URL: {state.get('pr_url', 'N/A')}")
    print(f"  Log entries: {len(state.get('execution_log', []))}")

    return state


def main():
    parser = argparse.ArgumentParser(
        description="Run the Vindicta autonomous swarm pipeline"
    )
    parser.add_argument("intent", help="Feature description to implement")
    parser.add_argument(
        "--mock",
        action="store_true",
        default=True,
        help="Use mock LLM provider (default: True)",
    )
    parser.add_argument(
        "--ollama",
        action="store_true",
        help="Use Ollama LLM provider (requires running Ollama)",
    )

    args = parser.parse_args()
    use_mock = not args.ollama

    run_pipeline(args.intent, use_mock=use_mock)


if __name__ == "__main__":
    main()

import sys
import os
import time

# Ensure src is in path - use insert to prioritize local source over installed package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vindicta_agents.swarm import nexus
from vindicta_agents.swarm.nexus import build_master_graph
from vindicta_agents.swarm.config import ShowcaseProvider

print(f"DEBUG: Loaded nexus from {nexus.__file__}")


def main():
    print("Initiating Swarm Showcase: Operation Health Check")

    # 1. Initialize Showcase Provider
    provider = ShowcaseProvider()

    config = {
        "configurable": {"thread_id": "showcase-run-003", "llm_provider": provider}
    }

    initial_state = {
        "intent": "Add a standardized health check feature to all domains."
    }

    print("\nPhase 1: Planning (PO -> Architect -> ADL)")

    # Build graph WITHOUT interrupt for automated showcase
    # We simulate the pause manually if needed, but for "Showcase" we want it to flow.
    swarm = build_master_graph(interrupt=False)

    try:
        # Execute start to finish
        for event in swarm.stream(initial_state, config=config):
            for node_name, state_update in event.items():
                # Check for Phase transition
                if node_name == "HumanReview":
                    print("\n  [DONE] Planning Complete.")
                    print("\n  Swarm Paused for Human Review")
                    print("  (Simulating User Approval...)")
                    time.sleep(2)
                    print("  Approved! Starting Execution Phase...\n")
                    print("\nPhase 2: Execution (Domain Agents -> Git)")
                    continue

                print(f"  [DONE] {node_name} completed.")

                if "spec_content" in state_update:
                    print(f"     [Spec]: {state_update['spec_content'][:50]}...")
                if "plan_content" in state_update:
                    print(f"     [Plan]: {state_update['plan_content'][:50]}...")
                if "tasks" in state_update:
                    print(
                        f"     [Tasks]: Generated {len(state_update['tasks'])} tasks."
                    )

                if "execution_log" in state_update:
                    for log in state_update["execution_log"]:
                        if "PR Created" in log:
                            print(f"     [PR] {log}")
                        else:
                            print(f"     [Log]: {log}")

        print("\nShowcase Complete!")
        print("Verify the PRs in GitHub.")

    except Exception as e:
        print(f"\nExecution Failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

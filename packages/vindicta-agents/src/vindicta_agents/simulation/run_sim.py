import asyncio
import argparse
import sys
from vindicta_agents.simulation.shadow_nexus import ShadowNexus
from vindicta_agents.simulation.scenarios import SCENARIO_BOUNDARY_VIOLATION
from vindicta_agents.utils.logger import logger

SCENARIOS = {"boundary_violation": SCENARIO_BOUNDARY_VIOLATION}


async def main():
    parser = argparse.ArgumentParser(
        description="Run a Shadow Mode Simulation Scenario"
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="boundary_violation",
        help="Name of the scenario to run",
    )
    args = parser.parse_args()

    if args.scenario not in SCENARIOS:
        logger.error(
            "scenario_not_found",
            scenario=args.scenario,
            available=list(SCENARIOS.keys()),
        )
        sys.exit(1)

    scenario = SCENARIOS[args.scenario]
    nexus = ShadowNexus()

    logger.info(
        "simulation_starting", scenario=scenario.name, description=scenario.description
    )

    report = await nexus.run_scenario(scenario)

    # We still want a readable report on the console
    print("\n" + "=" * 40)
    print(f"REPORT: {scenario.name}")
    print("=" * 40)

    if report["passed"]:
        print("STATUS: PASSED (All outcomes matched expectations)")
    else:
        print("STATUS: FAILED")

    print("-" * 40)
    print(f"{'TICK':<6} {'AGENT':<20} {'EXPECTED':<20} {'ACTUAL':<20} {'RESULT'}")
    print("-" * 40)

    for step in report["steps"]:
        result_icon = "[PASS]" if step["match"] else "[FAIL]"
        print(
            f"{step['tick']:<6} {step['agent']:<20} {step['expected']:<20} {step['actual']:<20} {result_icon}"
        )

    print("=" * 40 + "\n")

    logger.info("simulation_complete", passed=report["passed"])


if __name__ == "__main__":
    asyncio.run(main())

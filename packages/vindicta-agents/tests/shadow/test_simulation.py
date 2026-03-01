import pytest
from vindicta_agents.simulation.shadow_nexus import ShadowNexus
from vindicta_agents.simulation.scenarios import SCENARIO_BOUNDARY_VIOLATION


@pytest.mark.asyncio
async def test_shadow_boundary_violation():
    """
    Test the Boundary Violation Scenario in Shadow Mode.
    """
    nexus = ShadowNexus()
    report = await nexus.run_scenario(SCENARIO_BOUNDARY_VIOLATION)

    assert report["scenario"] == "Boundary Violation Test"
    assert report["passed"] is True, f"Scenario Failed: {report['steps']}"

    # Optional: Verify detailed steps
    steps = report["steps"]
    assert len(steps) == 3
    assert steps[0]["match"] is True  # Negative X -> Halt
    assert steps[1]["match"] is True  # Out of bounds X -> Halt
    assert steps[2]["match"] is True  # Valid -> Approval

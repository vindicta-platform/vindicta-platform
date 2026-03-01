from pydantic import BaseModel
from typing import Dict, Any, List


class ScenarioAction(BaseModel):
    agent_id: str
    tick: int
    action_type: str
    payload: Dict[str, Any]
    expected_outcome: str  # "AXIOM_APPROVAL", "CONSTITUTIONAL_HALT"


class Scenario(BaseModel):
    name: str
    description: str
    initial_state_delta: Dict[str, Any]
    actions: List[ScenarioAction]


# SCENARIO 1: The Out-of-Bounds Scout
# A scout unit tries to move to (-1, -1), which violates AX-02.
SCENARIO_BOUNDARY_VIOLATION = Scenario(
    name="Boundary Violation Test",
    description="A scout attempts to move outside the 44x60 board limits.",
    initial_state_delta={
        "units": {"scout-01": {"x": 5.0, "y": 5.0, "z": 0.0}},
        "phase": "MOVEMENT",
        "turn": 1,
    },
    actions=[
        ScenarioAction(
            agent_id="scout-agent-01",
            tick=1,
            action_type="move",
            payload={
                "units": {
                    "scout-01": {"x": -1.0, "y": 5.0, "z": 0.0}  # Invalid X
                }
            },
            expected_outcome="CONSTITUTIONAL_HALT",
        ),
        ScenarioAction(
            agent_id="scout-agent-01",
            tick=2,
            action_type="move",
            payload={
                "units": {
                    "scout-01": {"x": 45.0, "y": 5.0, "z": 0.0}  # Invalid X (Max 44)
                }
            },
            expected_outcome="CONSTITUTIONAL_HALT",
        ),
        ScenarioAction(
            agent_id="scout-agent-01",
            tick=3,
            action_type="move",
            payload={
                "units": {
                    "scout-01": {"x": 10.0, "y": 10.0, "z": 0.0}  # Valid
                }
            },
            expected_outcome="AXIOM_APPROVAL",
        ),
    ],
)

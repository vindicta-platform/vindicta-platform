"""SDD lifecycle scenarios for ShadowNexus simulation.

These scenarios validate the full autonomous workflow using
the existing ShadowNexus framework, but targeting the SDD pipeline
instead of the axiom-based supervisor scenarios.
"""

from __future__ import annotations

from vindicta_agents.simulation.scenarios import Scenario, ScenarioAction


def build_sdd_happy_path() -> Scenario:
    """Complete SDD lifecycle: specify → plan → tasks → implement → verify → merge."""
    return Scenario(
        name="SDD Happy Path",
        description="Full autonomous lifecycle with no rejections",
        initial_state_delta={
            "intent": "Add health check endpoint",
            "sdd_stage": "",
            "current_phase": "",
        },
        actions=[
            ScenarioAction(
                tick=1,
                agent_id="SM",
                action_type="boot",
                payload={"sdd_stage": "specify", "current_phase": "planning"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=2,
                agent_id="PO",
                action_type="generate_spec",
                payload={"spec_content": "Health check spec", "sdd_stage": "specify"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=3,
                agent_id="Architect",
                action_type="create_plan",
                payload={"plan_content": "Implementation plan", "sdd_stage": "plan"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=4,
                agent_id="ADL",
                action_type="generate_tasks",
                payload={
                    "tasks_content": "Task list",
                    "sdd_stage": "tasks",
                    "current_phase": "review",
                },
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=5,
                agent_id="SD",
                action_type="delegate",
                payload={"sdd_stage": "implement", "current_phase": "execution"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=6,
                agent_id="SD_Review",
                action_type="review_code",
                payload={"sdd_stage": "verify"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=7,
                agent_id="SM_Merge",
                action_type="merge",
                payload={"sdd_stage": "done", "current_phase": "done"},
                expected_outcome="AXIOM_APPROVAL",
            ),
        ],
    )


def build_sdd_decline_scenario() -> Scenario:
    """PO spec is declined, triggering memory + retry."""
    return Scenario(
        name="SDD Spec Decline",
        description="Spec rejected by human, PO regenerates with feedback",
        initial_state_delta={
            "intent": "Add caching layer",
            "sdd_stage": "",
            "current_phase": "",
        },
        actions=[
            ScenarioAction(
                tick=1,
                agent_id="SM",
                action_type="boot",
                payload={"sdd_stage": "specify", "current_phase": "planning"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=2,
                agent_id="PO",
                action_type="generate_spec",
                payload={"spec_content": "Vague spec", "sdd_stage": "specify"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=3,
                agent_id="HumanReview",
                action_type="decline_spec",
                payload={"decline_reason": "Too vague, missing AC"},
                expected_outcome="AXIOM_APPROVAL",
            ),
            ScenarioAction(
                tick=4,
                agent_id="PO",
                action_type="regenerate_spec",
                payload={
                    "spec_content": "Improved spec with AC",
                    "sdd_stage": "specify",
                },
                expected_outcome="AXIOM_APPROVAL",
            ),
        ],
    )


SDD_SCENARIOS = [
    build_sdd_happy_path(),
    build_sdd_decline_scenario(),
]

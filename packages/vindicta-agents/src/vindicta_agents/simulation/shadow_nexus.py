import uuid
from typing import Dict, Any, Optional
from vindicta_agents.supervisor.gatekeeper import AxiomaticSupervisor, AxiomApproval
from vindicta_agents.shared.memory import SharedMemory
from vindicta_agents.simulation.scenarios import Scenario
from vindicta_agents.utils.logger import FlightRecorder, logger


class ShadowNexus:
    """
    Simulated Nexus Orchestrator for Shadow Mode.
    Executes predefined scenarios to validate Supervisor logic.
    """

    def __init__(self, supervisor: Optional[AxiomaticSupervisor] = None):
        self.supervisor = supervisor or AxiomaticSupervisor()
        self.memory = SharedMemory()
        self.recorder = FlightRecorder()

    def load_scenario(self, scenario: Scenario):
        """
        Resets state and loads the scenario.
        """
        logger.info("loading_scenario", scenario=scenario.name)
        self.memory.reset()
        if scenario.initial_state_delta:
            self.memory.state.update(scenario.initial_state_delta)
        logger.debug("scenario_initial_state", state=str(self.memory.state))

    async def run_scenario(self, scenario: Scenario) -> Dict[str, Any]:
        """
        Executes actions in the scenario and verifies outcomes.
        Returns a report of pass/fail.
        """
        self.load_scenario(scenario)
        results = {"scenario": scenario.name, "passed": True, "steps": []}

        for action in scenario.actions:
            trace_id = str(uuid.uuid4())
            logger.info(
                "scenario_tick",
                tick=action.tick,
                agent_id=action.agent_id,
                action_type=action.action_type,
            )

            # 1. Propose State Transition (Simulated Agent Action)
            outcome = self.supervisor.verify_state_transition(
                trace_id=trace_id, proposed_delta=action.payload
            )

            # 2. Verify Outcome
            # Match against AXIOM_APPROVAL or CONSTITUTIONAL_HALT
            actual_type = (
                "AXIOM_APPROVAL"
                if isinstance(outcome, AxiomApproval)
                else "CONSTITUTIONAL_HALT"
            )
            match = actual_type == action.expected_outcome

            step_result = {
                "tick": action.tick,
                "agent": action.agent_id,
                "expected": action.expected_outcome,
                "actual": actual_type,
                "match": match,
                "trace_id": trace_id,
            }
            results["steps"].append(step_result)

            if not match:
                results["passed"] = False
                logger.error(
                    "step_failure",
                    expected=action.expected_outcome,
                    actual=actual_type,
                    tick=action.tick,
                )
            else:
                logger.info("step_success", outcome=actual_type, tick=action.tick)

        return results

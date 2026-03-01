from typing import Dict, Any, Union, Optional
from pydantic import BaseModel
from vindicta_agents.foundation.axioms import Dimensionality
from vindicta_agents.shared.memory import SharedMemory
from vindicta_agents.utils.logger import FlightRecorder


# Response Models
class AxiomApproval(BaseModel):
    approved: bool = True
    trace_id: str
    new_state_hash: str


class ConstitutionalHalt(BaseModel):
    approved: bool = False
    trace_id: str
    violation_code: str
    message: str


Outcome = Union[AxiomApproval, ConstitutionalHalt]


class AxiomaticSupervisor:
    """
    The Gatekeeper.
    Validates state transitions against Axioms.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AxiomaticSupervisor, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        memory: Optional[SharedMemory] = None,
        recorder: Optional[FlightRecorder] = None,
    ):
        if not hasattr(self, "memory"):
            self.memory = memory or SharedMemory()
            self.recorder = recorder or FlightRecorder()

    def verify_state_transition(
        self, trace_id: str, proposed_delta: Dict[str, Any]
    ) -> Outcome:
        """
        Validates a proposed state change.
        """
        _current_state = self.memory.state

        # AX-04: Temporal Discretization Checks
        # Example: Can't move in Combat phase (simplified)
        if "action" in proposed_delta:
            _action_type = proposed_delta["action"]  # e.g., "move", "attack"
            # If strictly enforcing phases, check here.
            # For now, we assume the delta implies a phase-appropriate action or phase change.

        # AX-02: Dimensionality Checks
        if "units" in proposed_delta:
            for unit_id, coords in proposed_delta["units"].items():
                try:
                    # Validate against Dimensionality Axiom
                    # This will raise ValueError if invalid
                    Dimensionality(**coords)
                except ValueError as e:
                    self.recorder.log_event(
                        trace_id=trace_id,
                        component="SUPERVISOR",
                        event_type="CONSTITUTIONAL_HALT",
                        details={
                            "violation": "AX-02",
                            "error": str(e),
                            "delta": proposed_delta,
                        },
                    )
                    return ConstitutionalHalt(
                        trace_id=trace_id,
                        violation_code="AX-02",
                        message=f"Dimensionality Violation for {unit_id}: {str(e)}",
                    )

        # If we reached here, it's valid.
        # Commit to Shared Memory
        self.memory.state.update(proposed_delta)

        # Log to Flight Recorder
        self.recorder.log_event(
            trace_id=trace_id,
            component="SUPERVISOR",
            event_type="AXIOM_APPROVAL",
            details={
                "new_version": str(self.memory.state.version),
                "delta": proposed_delta,
            },
        )

        return AxiomApproval(
            trace_id=trace_id, new_state_hash=str(self.memory.state.version)
        )

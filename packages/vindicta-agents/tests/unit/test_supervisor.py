from vindicta_agents.supervisor.gatekeeper import (
    AxiomaticSupervisor,
    AxiomApproval,
    ConstitutionalHalt,
)
from vindicta_agents.shared.memory import SharedMemory


def test_supervisor_singleton():
    s1 = AxiomaticSupervisor()
    s2 = AxiomaticSupervisor()
    assert s1 is s2


def test_interaction_with_shared_memory():
    supervisor = AxiomaticSupervisor()
    memory = SharedMemory()
    memory.reset()

    # Verify they point to same memory state
    assert supervisor.memory is memory


def test_valid_move():
    supervisor = AxiomaticSupervisor()
    SharedMemory().reset()

    delta = {"units": {"unit_1": {"x": 10.0, "y": 20.0, "z": 0.0}}}

    result = supervisor.verify_state_transition(trace_id="test-1", proposed_delta=delta)
    assert isinstance(result, AxiomApproval)
    assert result.approved is True

    # Verify memory updated
    assert SharedMemory().state.units["unit_1"]["x"] == 10.0


def test_invalid_move_out_of_bounds():
    supervisor = AxiomaticSupervisor()
    SharedMemory().reset()

    # X > 44 is invalid per AX-02
    delta = {"units": {"unit_1": {"x": 50.0, "y": 20.0, "z": 0.0}}}

    result = supervisor.verify_state_transition(trace_id="test-2", proposed_delta=delta)
    assert isinstance(result, ConstitutionalHalt)
    assert result.approved is False
    assert "AX-02" in result.violation_code

    # Verify memory NOT updated
    assert "unit_1" not in SharedMemory().state.units

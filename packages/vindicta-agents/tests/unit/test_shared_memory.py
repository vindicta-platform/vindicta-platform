from vindicta_agents.shared.memory import SharedMemory


def test_shared_memory_singleton():
    mem1 = SharedMemory()
    mem2 = SharedMemory()
    assert mem1 is mem2
    assert mem1.state is mem2.state


def test_board_state_update():
    mem = SharedMemory()
    mem.reset()
    initial_version = mem.state.version

    delta = {"phase": "Movement", "turn": 2}
    mem.state.update(delta)

    assert mem.state.phase == "Movement"
    assert mem.state.turn == 2
    assert mem.state.version != initial_version


def test_unit_update():
    mem = SharedMemory()
    mem.reset()

    unit_data = {"unit_1": {"x": 10, "y": 10}}
    mem.state.update({"units": unit_data})

    assert "unit_1" in mem.state.units
    assert mem.state.units["unit_1"]["x"] == 10

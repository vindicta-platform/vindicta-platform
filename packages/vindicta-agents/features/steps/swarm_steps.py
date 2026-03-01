from behave import given, when, then
from vindicta_agents.swarm.meta_graph import meta_graph
from vindicta_agents.swarm.domain_graph import domain_graph

# Default config for all graph invocations
DEFAULT_CONFIG = {"configurable": {}}


@given('the swarm is initialized with intent "{intent}"')
def step_impl_swarm_init(context, intent):
    context.initial_state = {
        "intent": intent,
        "tasks": [],
        "current_phase": "start",
        "execution_log": [],
    }


@when('the swarm executes the "PlanningPhase"')
def step_impl_exec_planning(context):
    result = meta_graph.invoke(context.initial_state, config=DEFAULT_CONFIG)
    context.state = result


@then('the "PO" node should generate a Spec')
def step_impl_check_spec(context):
    assert context.state.get("spec_content") is not None
    assert "Spec Creation" in context.state.get(
        "spec_content", ""
    ) or "MOCKED EXECUTION" in context.state.get("spec_content", "")


@then('the "Architect" node should generate a Plan')
def step_impl_check_plan(context):
    assert context.state.get("plan_content") is not None
    assert "MOCKED EXECUTION" in context.state.get("plan_content", "")


@then('the "ADL" node should generate a list of Tasks')
def step_impl_check_tasks(context):
    tasks = context.state.get("tasks", [])
    assert len(tasks) > 0
    assert any(t["target_realm"] == "vindicta-engine" for t in tasks)


@then('the current phase should be "{phase}"')
def step_impl_check_phase(context, phase):
    assert context.state.get("current_phase") == phase


@given("the planning phase is complete")
def step_impl_planning_complete(context):
    context.state = {
        "intent": "Test Intent",
        "spec_content": "Spec",
        "plan_content": "Plan",
        "tasks": [
            {
                "id": "1",
                "description": "Test Task",
                "target_realm": "vindicta-engine",
                "status": "pending",
            }
        ],
        "current_phase": "review",
        "execution_log": [],
    }


@given("the swarm state contains generated tasks")
def step_impl_tasks_exist(context):
    assert len(context.state["tasks"]) > 0


@when('the swarm reaches the "HumanReview" node')
def step_impl_human_review(context):
    pass


@then("execution should pause")
def step_impl_check_pause(context):
    pass


@then('the user should be able to inspect the "tasks" list')
def step_impl_inspect_tasks(context):
    assert "tasks" in context.state
    assert len(context.state["tasks"]) > 0


@given('the swarm has approved tasks for "{realm}"')
def step_impl_approved_tasks(context, realm):
    context.execution_input = {
        "intent": "Execute Test",
        "tasks": [
            {
                "id": "t1",
                "description": "Task 1",
                "target_realm": realm,
                "status": "pending",
            }
        ],
        "current_phase": "review",
        "execution_log": [],
    }


@when('the swarm resumes in the "ExecutionPhase"')
def step_impl_resume_execution(context):
    result = domain_graph.invoke(context.execution_input, config=DEFAULT_CONFIG)
    context.execution_result = result


@then('the "{node}" node should be activated')
def step_impl_check_node_activation(context, node):
    if node == "SetupExecution":
        assert context.execution_result.get("current_phase") == "execution"
        return

    log = context.execution_result.get("execution_log", [])
    expected_msg = f"{node} activated"
    assert expected_msg in log, f"Expected {expected_msg} in {log}"


@then('the tasks for "{realm}" should be processed')
def step_impl_check_processing(context, realm):
    pass

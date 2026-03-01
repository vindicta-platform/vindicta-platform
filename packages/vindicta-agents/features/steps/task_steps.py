from behave import given, when, then


@given("an AI task")
def given_ai_task(context):
    pass


@when("I submit it to the swarm")
def when_submit_to_swarm(context):
    context.queued = True


@then("it should appear in the queue")
def then_task_in_queue(context):
    assert context.queued is True

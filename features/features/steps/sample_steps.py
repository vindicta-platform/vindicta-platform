from behave import given, when, then


@given("the testing environment is set up")
def step_impl(context):
    pass


@when("I run this sample test")
def step_impl(context):
    pass


@then("it should pass successfully")
def step_impl(context):
    assert True

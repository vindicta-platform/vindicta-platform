from behave import given, when, then


@given("a user with 100 credits")
def given_user_with_100_credits(context):
    context.balance = 100


@when("they spend 10 credits")
def when_spend_10_credits(context):
    context.balance -= 10


@then("their balance should be 90 credits")
def then_balance_is_90(context):
    assert context.balance == 90

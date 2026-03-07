# BDD Workflow Reference

## Gherkin Syntax Quick Reference

```gherkin
Feature: <Feature Name>
  As a <role>
  I want <goal>
  So that <benefit>

  Background:
    Given <shared precondition for all scenarios>

  Scenario: <Scenario Name>
    Given <initial state>
    And <additional context>
    When <action>
    Then <expected result>
    And <additional assertion>
    But <negative assertion>

  Scenario Outline: <Parameterized Scenario>
    Given <state with <param>>
    When <action with <param>>
    Then <expected <result>>

    Examples:
      | param  | result  |
      | value1 | output1 |
      | value2 | output2 |
```

## Behave Step Definition Patterns

```python
from behave import given, when, then

@given('a unit with {health:d} health')
def step_unit_health(context, health):
    context.unit = Unit(health=health)

@when('the unit takes {damage:d} damage')
def step_unit_takes_damage(context, damage):
    context.unit.take_damage(damage)

@then('the unit has {expected:d} health remaining')
def step_unit_health_remaining(context, expected):
    assert context.unit.health == expected
```

## Vindicta BDD Structure

```text
packages/features/
├── axioms.feature         # Zero-Order Axiom validation
├── economy.feature        # Gas tank & ledger scenarios
├── combat.feature         # Combat resolution scenarios
├── steps/                 # Python step definitions
│   ├── test_axioms.py
│   ├── test_economy.py
│   └── test_combat.py
└── environment.py         # Behave hooks & context setup
```

## Key Commands

| Goal                     | Command                                     |
| :----------------------- | :------------------------------------------ |
| Run all features         | `uv run behave packages/features/`          |
| Run specific feature     | `uv run behave packages/features/x.feature` |
| Run by tag               | `uv run behave --tags=@smoke`               |
| Dry run (check syntax)   | `uv run behave --dry-run`                   |
| Verbose output           | `uv run behave -v`                          |

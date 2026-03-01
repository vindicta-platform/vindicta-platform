Feature: Zero-Order Axioms
  As the Swarm Architect
  I want to enforce the fundamental laws of the Vindicta simulation
  So that the simulation remains consistent and error-free

  Scenario: Entity Identity must be unique and time-dependent
    Given a new entity is created
    When I request its identity
    Then it should have a valid UUID
    And its state should include a timestamp

  Scenario: Dimensionality Checks - Valid Coordinates
    Given an entity at coordinates (10, 20, 0)
    When I validate its position
    Then the position should be valid

  Scenario: Dimensionality Checks - Negative Coordinates Violation
    Given an entity at coordinates (-5, 10, 0)
    When I validate its position
    Then it should raise a Constitutional Violation error

  Scenario: Dimensionality Checks - Out of Bounds
    Given an entity at coordinates (100, 100, 0)
    When I validate its position
    Then it should raise a Constitutional Violation error because the bounds are 44x60

  Scenario: Probability Source Traceability
    Given a random outcome is generated
    When I inspect the outcome
    Then it should reference the Central Entropy Provider

  Scenario: Temporal Discretization
    Given the system is in Phase 1
    When I attempt an action in Phase 1.5
    Then it should be rejected because steps are discrete

Feature: Axiomatic Governance
  As the Axiomatic Supervisor
  I want to validate every state transition against the Constitution
  So that no agent can violate the laws of physics or the rules of the game

  Scenario: Valid State Transition
    Given the current board state is valid
    When an agent proposes a move to (10, 10, 0)
    And the move is within bounds
    And the current phase allows movement
    Then the Supervisor should issue an "AxiomApproval"
    And the state should be updated

  Scenario: Constitutional Violation - Out of Bounds
    Given the current board state is valid
    When an agent proposes a move to (50, 50, 0)
    Then the Supervisor should issue a "ConstitutionalHalt"
    And the error should cite "AX-02: Dimensionality Violation"
    And the state should NOT be updated

  Scenario: Constitutional Violation - Wrong Phase
    Given the current phase is "Combat"
    When an agent proposes a "Movement" action
    Then the Supervisor should issue a "ConstitutionalHalt"
    And the error should cite "AX-04: Temporal Discretization Violation"

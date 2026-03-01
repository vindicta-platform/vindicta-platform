Feature: Human Review Gates
  As a human reviewer
  I want approve/decline gates at key pipeline stages
  So that I can control spec quality, plan review, and PR merge decisions

  # --- Spec Review Gate ---

  Scenario: Reviewer approves a spec
    Given a spec is ready for review
    When the reviewer selects "Approve"
    Then the spec should be forwarded to the Architect
    And sdd_stage should advance to "plan"

  Scenario: Reviewer declines a spec with reason
    Given a spec is ready for review
    When the reviewer selects "Decline"
    And provides reason "Missing acceptance criteria"
    Then the spec should be removed from the queue
    And the decline memory should contain "Missing acceptance criteria"
    And the PO should be notified to regenerate

  # --- Plan Review Gate ---

  Scenario: Reviewer approves a plan
    Given tasks have been generated from a plan
    When the reviewer selects "Approve" at the plan review gate
    Then the pipeline should advance to execution

  Scenario: Reviewer declines a plan
    Given tasks have been generated from a plan
    When the reviewer selects "Decline" at the plan review gate
    And provides reason "Tasks too coarse-grained"
    Then the pipeline should loop back to the Architect

  # --- PR Merge Gate ---

  Scenario: Reviewer approves PR merge
    Given a PR has been created and reviewed by SSE
    When the reviewer selects "Merge"
    Then the PR should be merged via GitHub API
    And sdd_stage should be "done"

  Scenario: Reviewer declines PR merge
    Given a PR has been created and reviewed by SSE
    When the reviewer selects "Decline"
    And provides reason "Test coverage insufficient"
    Then the PR should remain open
    And the feedback should be logged

  # --- Review Gate Abstraction ---

  Scenario: ReviewGate returns approve decision
    Given a ReviewGate configured with approve/decline options
    When the decision is "approve"
    Then the gate result should have approved=True

  Scenario: ReviewGate returns decline with reason
    Given a ReviewGate configured with approve/decline options
    When the decision is "decline" with reason "Needs more detail"
    Then the gate result should have approved=False
    And the gate result reason should be "Needs more detail"

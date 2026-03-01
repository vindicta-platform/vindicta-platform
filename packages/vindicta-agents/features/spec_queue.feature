Feature: Spec Queue & Decline Memory
  As the Swarm Orchestrator
  I want a spec queue that the PO fills and a decline memory that feeds back
  So that specs are produced ahead of execution and rejected specs improve

  # --- SpecQueue basics ---

  Scenario: Queue starts empty
    Given an empty spec queue with target size 5
    Then the queue size should be 0
    And the queue should not be full

  Scenario: Add specs to the queue
    Given an empty spec queue with target size 5
    When the PO adds a spec "feature-auth" with content "Auth spec"
    And the PO adds a spec "feature-cache" with content "Cache spec"
    Then the queue size should be 2
    And the queue should not be full

  Scenario: Queue reports full at target size
    Given a spec queue pre-filled with 5 specs
    Then the queue should be full

  Scenario: Pop removes the oldest spec
    Given an empty spec queue with target size 5
    And the PO adds a spec "first" with content "A"
    And the PO adds a spec "second" with content "B"
    When I pop a spec from the queue
    Then the popped spec should have feature name "first"
    And the queue size should be 1

  Scenario: Pop from empty queue returns None
    Given an empty spec queue with target size 5
    When I pop a spec from the queue
    Then the popped spec should be None

  # --- Decline Memory ---

  Scenario: Decline a spec stores reason in memory
    Given an empty spec queue with target size 5
    And an empty decline memory
    When I decline spec "feature-bad" with reason "Too vague"
    Then the decline memory should contain 1 record
    And the latest decline reason should be "Too vague"

  Scenario: Decline memory provides history for PO prompt
    Given an empty decline memory
    And I decline spec "spec-1" with reason "Missing acceptance criteria"
    And I decline spec "spec-2" with reason "Scope too broad"
    When I retrieve the decline history
    Then the history should contain 2 records
    And the history should include reason "Missing acceptance criteria"
    And the history should include reason "Scope too broad"

  # --- Extended State ---

  Scenario: VindictaState includes SDD lifecycle fields
    Given a fresh VindictaState
    Then it should have field "sdd_stage"
    And it should have field "feature_name"
    And it should have field "branch_name"
    And it should have field "spec_queue"
    And it should have field "decline_memory"
    And it should have field "pr_url"
    And it should have field "issue_urls"

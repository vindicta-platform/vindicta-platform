Feature: Autonomous SDD Workflow
  As the Vindicta Swarm
  I want agents to execute the full SDD lifecycle autonomously
  So that specs are created, planned, implemented, reviewed, and merged via PRs

  # --- PO Node ---

  Scenario: PO generates a spec when queue has slots
    Given a swarm with an empty spec queue
    And a mocked LLM provider
    When the PO node runs
    Then the spec queue should have at least 1 item
    And the execution log should contain "PO: generated spec"

  Scenario: PO uses decline memory to avoid repeating mistakes
    Given a swarm with decline memory containing "Too vague"
    And a mocked LLM provider
    When the PO node runs
    Then the LLM prompt should include "Too vague"

  # --- Architect Node ---

  Scenario: Architect clarifies and plans from a spec
    Given a swarm with spec_content set
    And a mocked LLM provider
    When the Architect node runs
    Then plan_content should be set
    And the execution log should contain "Architect: plan created"

  # --- ADL Node ---

  Scenario: ADL generates tasks from a plan
    Given a swarm with plan_content set
    And a mocked LLM provider
    When the ADL node runs
    Then tasks_content should be set
    And tasks should contain at least 1 task
    And the execution log should contain "ADL: tasks generated"

  # --- SD Node ---

  Scenario: SD delegates tasks to domain agents by realm
    Given a swarm with pending tasks for "vindicta-engine" and "warscribe-system"
    When the SD node runs
    Then TechPriest should receive vindicta-engine tasks
    And LogosHistorian should receive warscribe-system tasks
    And the execution log should contain "SD: delegated"

  # --- Domain Agents ---

  Scenario: TechPriest writes code for assigned task
    Given a TechPriest with mocked LLM and file tools
    And a task assigned to "vindicta-engine"
    When the TechPriest node runs
    Then the task should have a code_diff
    And the task status should be "completed"

  # --- SD Review ---

  Scenario: SD Review approves good diffs
    Given completed tasks with code diffs
    And a mocked LLM that approves
    When the SD Review node runs
    Then the execution log should contain "SD_Review: approved"

  # --- SSE Node ---

  Scenario: SSE creates a PR after final review
    Given all tasks completed and reviewed
    And a mocked GitHub client
    When the SSE node runs
    Then pr_url should be set
    And the execution log should contain "SSE: PR created"

  # --- SM Node ---

  Scenario: SM boots the swarm with priorities
    Given a fresh swarm state
    When the SM node runs
    Then sdd_stage should be "specify"
    And the execution log should contain "SM: swarm booted"

  Scenario: SM merges an approved PR
    Given a swarm with pr_url set
    And a mocked GitHub client
    When the SM Merge node runs
    Then sdd_stage should be "done"
    And the execution log should contain "SM: PR merged"

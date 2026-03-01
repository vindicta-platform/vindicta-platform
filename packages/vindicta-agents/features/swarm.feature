Feature: LangGraph Swarm Orchestration
  As the Master Architect
  I want the swarm to autonomously plan and execute tasks using a hierarchical graph
  So that I can leverage specialized agents for different repositories

  Scenario: Successful Planning Phase
    Given the swarm is initialized with intent "Refactor the engine"
    When the swarm executes the "PlanningPhase"
    Then the "PO" node should generate a Spec
    And the "Architect" node should generate a Plan
    And the "ADL" node should generate a list of Tasks
    And the current phase should be "review"

  Scenario: Human-in-the-Loop Interruption
    Given the planning phase is complete
    And the swarm state contains generated tasks
    When the swarm reaches the "HumanReview" node
    Then execution should pause
    And the user should be able to inspect the "tasks" list

  Scenario: Domain Execution Routing to TechPriest
    Given the swarm has approved tasks for "vindicta-engine"
    When the swarm resumes in the "ExecutionPhase"
    Then the "TechPriest" node should be activated
    And the tasks for "vindicta-engine" should be processed

  Scenario: Domain Execution Routing to LogosHistorian
    Given the swarm has approved tasks for "warscribe-system"
    When the swarm resumes in the "ExecutionPhase"
    Then the "LogosHistorian" node should be activated
    And the tasks for "warscribe-system" should be processed

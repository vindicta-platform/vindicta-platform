Feature: Void Banker Management
  As the Resource Governor
  I want to manage compute credits and enforce resource policies
  So that the server hardware is protected and prioritized tasks are completed

  Background:
    Given the Void Banker is initialized with a clean ledger
    And an agent "tech_priest" exists with a balance of 100 CC

  Scenario: Successful Compute Expenditure
    When "tech_priest" performs a "bsh_generation" operation
    Then their balance should be 99 CC
    And the transaction should be logged in the ledger

  Scenario: Alpha-Beta Search Exponential Cost
    When "tech_priest" performs an "alpha_beta_search" at depth 3
    Then their balance should be 92 CC

  Scenario: Insolvency Enforcement
    Given the agent "tech_priest" has a balance of 2 CC
    When "tech_priest" attempts a "dmf_evaluation" operation
    Then the operation should be denied
    And their balance should remain 2 CC

  Scenario: Thermal Guard Protection
    Given the system temperature is 90 degrees
    When "tech_priest" attempts any operation
    Then a "THERMAL GUARD" should be issued
    And no credits should be deducted from "tech_priest"

  Scenario: Load Shedding Prioritization
    Given the system load is 95 percent
    When "tech_priest" attempts a "BACKGROUND_SIMULATION" task
    Then the operation should be denied due to "LOAD SHEDDING"
    But when "tech_priest" attempts a "LIVE_GAME_STATE" task
    Then the operation should be allowed

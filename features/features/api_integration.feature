Feature: Engine Economy Integration
  As a Vindicta Platform operator
  I want to ensure all tactical engines are wired with an Economy Subsystem
  So that I can enforce compute credit limits and maintain the Gas Tank model

  Scenario: Tactical Engine rejects execution without credits
    Given a tactical engine wired with the Platform Economy Client
    And an agent "malicious_user" with "0" credits
    When the engine is asked to "evaluate_state" for "malicious_user"
    Then it should raise an "InsolvencyError"
    And no engine computation should be performed

  Scenario: Tactical Engine succeeds with sufficient credits
    Given a tactical engine wired with the Platform Economy Client
    And an agent "premium_user" with "100" credits
    When the engine is asked to "evaluate_state" for "premium_user"
    Then the engine should return a valid evaluation
    And credit balance for "premium_user" should be reduced by "1"

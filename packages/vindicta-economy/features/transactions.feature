Feature: Transactions
  Scenario: Record a spend
    Given a user with 100 credits
    When they spend 10 credits
    Then their balance should be 90 credits

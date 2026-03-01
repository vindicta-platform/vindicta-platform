Feature: Task Queue
  Scenario: Add task to queue
    Given an AI task
    When I submit it to the swarm
    Then it should appear in the queue

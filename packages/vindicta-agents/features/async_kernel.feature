Feature: Async Nexus Communication
  As the Nexus Orchestrator
  I want to facilitate communication between agents using WebSockets
  So that the swarm can coordinate actions in real-time

  Scenario: Agent Connection
    Given the Nexus server is running
    When an agent connects via WebSocket
    And sends a valid Handshake message
    Then the connection should be accepted
    And the agent should be added to the Registry

  Scenario: WARScribe Envelope Validation
    Given an established WebSocket connection
    When an agent sends a message with a malformed envelope
    Then the Nexus should reject the message with an error
    And the rejection should be logged

  Scenario: Message Routing
    Given two agents "Tech-Priest" and "Logos-Historian" are connected
    When "Tech-Priest" sends a message addressed to "Logos-Historian"
    Then "Logos-Historian" should receive the message
    And the Trace ID should be preserved

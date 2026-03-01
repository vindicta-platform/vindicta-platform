Feature: Agent Initialization and Handshake
  As the Nexus Orchestrator
  I want to verify every agent that attempts to join the swarm
  So that only authorized and correctly configured agents can participate

  Scenario: Successful Agent Registration
    Given a valid agent configuration with Class "Tech-Priest" and Realm "vindicta-engine"
    When the agent initiates the handshake
    Then the agent should be registered with the Nexus
    And the agent status should be "Online"

  Scenario: Invalid Agent Class Registration
    Given an agent configuration with an unknown Class "Chaos-Spawn"
    When the agent initiates the handshake
    Then the handshake should fail
    And the agent should not be registered

  Scenario: Agent without Realm
    Given an agent configuration with no Realm specified
    When the agent initiates the handshake
    Then the handshake should fail due to missing Realm

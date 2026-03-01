Feature: Langfuse Agent Observability
  In order to track LLM token consumption and execution traces
  As a developer
  I want a local Langfuse server to capture all LLM interaction events

  @observability @llm
  Scenario: Agent logic triggers a trace event
    Given the local Langfuse server is running via docker-compose
    When the "Primordia-AI" logic invokes a chat completion
    Then the corresponding trace and prompts should be logged in Langfuse
    And the token usage should be recorded against the current session

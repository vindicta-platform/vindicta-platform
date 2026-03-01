Feature: Tool Infrastructure
  As the Swarm Orchestrator
  I want a set of tools for file operations, Git, GitHub, and LLM inference
  So that agents can autonomously interact with the codebase and external services

  # --- File Operations ---

  Scenario: Write and read a file
    Given a clean workspace directory
    When I write "hello world" to "test.txt"
    Then reading "test.txt" should return "hello world"

  Scenario: List directory contents
    Given a clean workspace directory
    And I write "a" to "file_a.txt"
    And I write "b" to "file_b.txt"
    When I list the workspace directory
    Then the listing should contain "file_a.txt"
    And the listing should contain "file_b.txt"

  Scenario: Create nested directories
    Given a clean workspace directory
    When I create directory "sub/nested/deep"
    Then the directory "sub/nested/deep" should exist

  Scenario: File operations respect workspace boundary
    Given a clean workspace directory
    When I attempt to write outside the workspace
    Then a sandbox violation error should be raised

  # --- Git Operations (GitPython) ---

  Scenario: Create and switch to a feature branch
    Given a Git repository in the workspace
    When I create branch "feature/test-branch"
    Then the current branch should be "feature/test-branch"

  Scenario: Stage and commit files
    Given a Git repository in the workspace
    And I write "content" to "new_file.py"
    When I stage "new_file.py"
    And I commit with message "feat: add new file"
    Then the last commit message should be "feat: add new file"

  Scenario: Check if branch exists
    Given a Git repository in the workspace
    And branch "feature/existing" exists
    When I check if branch "feature/existing" exists
    Then the result should be true

  # --- GitHub Operations (PyGithub) ---

  Scenario: Create a GitHub issue
    Given a configured GitHub client
    When I create an issue titled "Test Issue" with body "Test body" in "vindicta-platform/Vindicta-Agents"
    Then the issue should be created successfully
    And the issue should have the title "Test Issue"

  Scenario: Create a Pull Request
    Given a configured GitHub client
    When I create a PR titled "Test PR" from "feature/test" to "main" in "vindicta-platform/Vindicta-Agents"
    Then the PR should be created successfully

  Scenario: List issues with label filter
    Given a configured GitHub client
    And there are issues labelled "autonomous-swarm" in "vindicta-platform/Vindicta-Agents"
    When I list issues with label "autonomous-swarm"
    Then the result should contain issues with that label

  # --- LLM Operations (Ollama) ---

  Scenario: Generate text from a prompt
    Given an Ollama LLM provider
    When I generate text with system "You are helpful" and prompt "Say hello"
    Then the response should be a non-empty string

  Scenario: Generate structured JSON from a prompt
    Given an Ollama LLM provider
    When I generate JSON with prompt "Return a JSON object with key 'status' and value 'ok'"
    Then the response should be a dict containing key "status"

  # --- Tool Registry ---

  Scenario: Register and look up tools
    Given an empty tool registry
    When I register a tool named "file_read" with a callable
    Then looking up "file_read" should return that callable

  Scenario: Looking up unregistered tool raises error
    Given an empty tool registry
    When I look up "nonexistent_tool"
    Then a tool not found error should be raised

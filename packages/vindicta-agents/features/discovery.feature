Feature: Meso-Repo Discovery
  As the Control Plane
  I want to detect the presence of all meso-repositories
  So that I can interact with the entire platform

  Scenario: All Meso-Repos Present
    Given the 7 meso-repositories exist in the sibling directories
    When I run the discovery utility
    Then it should return verified paths for all 7 repositories
    And the status should be "Complete"

  Scenario: Missing Meso-Repo
    Given the "vindicta-engine" repository is missing from the filesystem
    When I run the discovery utility
    Then it should identify "vindicta-engine" as missing
    And the discovery status should be "Incomplete"

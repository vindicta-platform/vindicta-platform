$ErrorActionPreference = "Stop"

# Import Module
Import-Module "$PSScriptRoot\..\automation\modules\VindictaAgents.Automation.psm1" -Force

Describe "VindictaAgents.Automation Unit Tests" {

    Context "Unit: Logic Functions" {
        It "Calculates Week 1 correctly" {
            $date = [DateTime]"2026-02-05" # Day 2
            $week = Get-VindictaWeek -CurrentDate $date
            $week | Should Be 1
        }

        It "Calculates Week 2 correctly" {
            $date = [DateTime]"2026-02-12" # Day 9
            $week = Get-VindictaWeek -CurrentDate $date
            $week | Should Be 2
        }
    }
}

Describe "VindictaAgents.Automation Mock Tests" {

    # Run inside module scope so mocks overlay the external commands correctly
    InModuleScope "VindictaAgents.Automation" {

        Context "Mock: GitHub Integration" {
            # Define 'gh' as a function to mock the external command
            function gh { $global:LASTEXITCODE = 0; return "42" }

            It "Parses issue count from gh output" {
                $count = Get-GitHubIssues -Query "org:test"
                $count | Should Be 42
            }
        }

        Context "Mock: SDK Integration" {
            # Define 'python' as a function to mock the external command
            function python {
                $global:LASTEXITCODE = 0
                return '{ "task_id": "123", "status": "queued" }'
            }

            It "Submits task and parses JSON result" {
                $result = Submit-AgentTask -Prompt "Test Task"
                $result.task_id | Should Be "123"
                $result.status | Should Be "queued"
            }
        }

        Context "Mock: Reporting Logic" {
            # Mock file operations via native command mocking if possible, or assume paths are valid
            # In Pester 3, mocking Set-Content might be tricky if it's not a function.
            # But we can try mocking the *calls* if the module uses cmdlets.
            # NOTE: Pester 3 Mocking of cmdlets like Set-Content works.

            Mock Test-Path { return $true }
            Mock Get-Content { return "# Report`n## Activity Log`n- Old Entry" }
            Mock Set-Content { }
            Mock New-Item { }

            It "Update-AgentReport calls Set-Content with appended log" {
                Update-AgentReport -AgentName "TestAgent" -Status "OK" -ActivityEntry "New Action"
                Assert-MockCalled Set-Content -Times 1
            }
        }

        Context "Mock: GitHub Sync" {
            # Override gh for sync
            function gh {
                $global:LASTEXITCODE = 0
                # Issue Search: gh issue list
                if ($args[1] -match "list") { return '[{"url":"https://github.com/org/repo/issues/1"}]' }
                # Issue Comment: gh issue comment
                if ($args[1] -match "comment") { return "https://github.com/org/repo/issues/1#comment" }
                return ""
            }

            It "Sync-GitHubEntity finds issue and comments" {
                $result = Sync-GitHubEntity -Query "test" -CommentBody "Update"
                $result | Should Be $true
            }

            It "Sync-GitHubEntity returns false if no issue found" {
                # Override gh to return empty list
                function gh {
                    $global:LASTEXITCODE = 0
                    if ($args[1] -match "list") { return '[]' }
                    return ""
                }

                $result = Sync-GitHubEntity -Query "missing" -CommentBody "Update"
                $result | Should Be $false
            }

            It "Sync-GitHubEntity handles GitHub CLI error gracefully" {
                # Override gh to simulate error
                function gh {
                    $global:LASTEXITCODE = 1
                    throw "GH API Error"
                }
                $result = Sync-GitHubEntity -Query "error" -CommentBody "Update"
                $result | Should Be $false
            }
        }
    }
}

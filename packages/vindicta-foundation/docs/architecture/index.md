# Vindicta Platform — Architecture

> **Single entrypoint for the platform's architectural footprint.**
> All diagrams are generated to match the [C4-Target-State.md](C4-Target-State.md) blueprint.

---

## System Context (C4 Level 1)

```mermaid
C4Context
    title Vindicta Platform — System Context

    Person(player, "Competitive Player", "Builds lists, tracks matches, analyzes the meta")
    Person(to, "Tournament Organizer", "Runs events, manages pairings, reviews results")
    Person(admin, "Platform Admin", "Maintains infrastructure, monitors health, evolves the platform")

    System(vindicta, "Vindicta Platform", "Unified competitive Warhammer 40k platform for army management, match tracking, meta analysis, and AI predictions")

    System_Ext(gcp, "Google Cloud Platform", "Hosting, databases, cloud services")
    System_Ext(github, "GitHub", "Source control, CI/CD, project management")

    Rel(player, vindicta, "Uses", "HTTPS, CLI")
    Rel(to, vindicta, "Manages tournaments via", "HTTPS")
    Rel(admin, vindicta, "Administers and evolves", "CLI, GitHub")
    Rel(vindicta, gcp, "Deployed to")
    Rel(vindicta, github, "Source-controlled and built via")
```

---

## Container Overview (C4 Level 2)

```mermaid
C4Container
    title Vindicta Platform — Container Overview

    Person(player, "Competitive Player")
    Person(admin, "Platform Admin")

    System_Boundary(vindicta, "Vindicta Platform") {

        Boundary(presentation, "Presentation") {
            Container(portal, "Vindicta-Portal", "HTML/JS", "Web portal for players")
            Container(ui, "Logi-Slate-UI", "React, Tailwind", "Component library")
            Container(cli, "Vindicta-CLI", "Python, Click", "Unified CLI")
            Container(api, "Vindicta-API", "Python, FastAPI", "REST API gateway")
        }

        Boundary(gamesim, "Game Simulation") {
            Container(dice, "Dice-Engine", "Python", "CSPRNG dice with entropy proofs")
            Container(entropy, "Entropy-Buffer", "Python", "Thread-safe RNG seeding")
        }

        Boundary(notation, "Game Notation") {
            Container(wsc, "WARScribe-Core", "Python", "WNS notation engine")
            Container(wsp, "WARScribe-Parser", "Python", "High-level WNS parsing")
            Container(wscli, "WARScribe-CLI", "Python", "Transcript ingestion CLI")
            Container(btt, "Battle-Transcript-Toolkit", "Python", "Agent transcript tools")
        }

        Boundary(analytics, "Analytics") {
            Container(oracle, "Meta-Oracle", "Python", "AI meta analysis and prediction")
        }

        Boundary(primordia, "Primordia") {
            Container(primordiaAI, "Primordia-AI", "Python", "Deterministic tactical AI")
            Container(arbiter, "Arbiter-Predictor", "Python", "Win probability statistics")
        }

        Boundary(platform, "Platform Services") {
            Container(core, "Vindicta-Core", "Python", "Shared primitives and config")
            Container(economy, "Economy-Engine", "Python", "Gas Tank, Ledger, Meter")
            Container(quota, "Quota-Manager", "Python", "Usage tracking and enforcement")
            Container(metered, "Metered-SaaS-Logic", "Python", "Dynamic pricing logic")
            Container(audit, "Audit-Log-Pro", "Python", "Dual-sink audit logging")
            Container(ledger, "Atomic-Ledger-Py", "Python", "Atomic ledger pattern")
            Container(auditor, "Agent-Auditor-SDK", "Python", "Mechanical Auditor framework")
        }

        Boundary(devex, "Developer Experience") {
            Container(docs, "Platform-Docs", "MkDocs", "Architecture and guides")
            Container(ghorg, ".github", "YAML", "Org config and templates")
            Container(specify, ".specify", "Markdown", "SDD constitution")
            Container(agent, ".agent", "YAML", "Agent workflows")
            Container(agents, "Vindicta-Agents", "Docker", "Dev container images")
        }
    }

    Rel(player, portal, "Browses", "HTTPS")
    Rel(player, cli, "Power-user access", "Terminal")
    Rel(admin, cli, "Platform ops", "Terminal")
    Rel(admin, docs, "Reads architecture", "HTTPS")
    Rel(portal, api, "Calls", "REST/JSON")
    Rel(cli, api, "Calls", "REST/JSON")
    Rel(api, dice, "Requests dice rolls")
    Rel(api, oracle, "Requests predictions")
    Rel(api, wsc, "Processes notation")
    Rel(api, quota, "Enforces quotas")
    Rel(dice, entropy, "Seeds from")
    Rel(oracle, arbiter, "Uses win probability")
    Rel(primordiaAI, dice, "Simulates via")
    Rel(wsp, wsc, "Parses via")
```

---

## Domain Views

Navigate to domain-specific architecture views:

| Domain                                            | Description                                    | Key Repos                                                                                                            |
| Domain              | Description                       | Key Repos                          |
| ------------------- | --------------------------------- | ---------------------------------- |
| **[Gateways](#)**   | User interfaces and Agent ingress | vindicta-platform, vindicta-agents |
| **[Physics](#)**    | Simulation, rules, dice, logs     | vindicta-engine, warscribe-system  |
| **[Meta](#)**       | Economy and debate council        | vindicta-economy, vindicta-oracle  |
| **[Foundation](#)** | Shared truth                      | vindicta-foundation                |

---

## Evolution Status

See [evolution.md](./evolution.md) for per-repo maturity tracking and tech radar status.

---

*Generated from the canonical C4-Target-State.*

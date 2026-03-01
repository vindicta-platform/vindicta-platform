# C4 Model: Target Architecture State

This document diagrams the target state of the Vindicta Platform after the consolidation of 29 existing repositories into 7 logical Meso-repos.

## Context Diagram

```mermaid
C4Context
    title System Context diagram for Vindicta Platform Target State

    Person(user, "User", "A player, tournament organizer, or developer")
    System(vindicta, "Vindicta Platform", "The complete wargaming e-sports platform")
    System_Ext(firebase, "Firebase", "Auth, Hosting, Remote Config")
    System_Ext(gcp, "Google Cloud Platform", "Cloud Run, Pub/Sub, Storage")

    Rel(user, vindicta, "Uses", "HTTPS/WSS")
    Rel(vindicta, firebase, "Authenticates via")
    Rel(vindicta, gcp, "Runs on")
```

## Container Diagram

The 7 consolidated repositories form the core containers of the system.

```mermaid
C4Container
    title Container diagram for Vindicta Platform Target State

    Person(user, "User", "A player or tournament organizer")

    Container_Boundary(vindicta_platform_boundary, "Vindicta Platform Organization") {
        
        Container(foundation, "vindicta-foundation", "Python/Pydantic", "Shared Kernel: Base Models, Architecture, Constitution. Single Source of Truth.")
        
        Container(platform, "vindicta-platform", "Python (API) / JS (Portal)", "User Interface, API Gateway, and Identity Management.")
        
        Container(engine, "vindicta-engine", "Python", "Physics, Dice Engine, Core Game Logic, and Simulation.")
        
        Container(scribe, "warscribe-system", "Python/AI", "Notation Parsing, Game State Reconstruction, and OCR/Vision.")
        
        Container(economy, "vindicta-economy", "Python", "Atomic Ledger, Quota Management, and 'Gas Tank' Billing.")
        
        Container(oracle, "vindicta-oracle", "Python/ML", "Predictive Models, Meta Analysis, and List Grading.")
        
        Container(agents, "vindicta-agents", "Python SDK", "Autonomous Agents, Swarm Infrastructure, and Auditor SDK.")
    }

    Rel(user, platform, "Interacts with", "HTTPS/WSS")

    %% Foundation Dependencies (All depend on Foundation)
    Rel(platform, foundation, "Inherits Models")
    Rel(engine, foundation, "Inherits Models")
    Rel(scribe, foundation, "Inherits Models")
    Rel(economy, foundation, "Inherits Models")
    Rel(oracle, foundation, "Inherits Models")
    Rel(agents, foundation, "Inherits Models")

    %% Core Workflows
    Rel(platform, engine, "Simulates games via", "Internal API")
    Rel(platform, scribe, "Parses uploaded logs via", "Pub/Sub")
    Rel(platform, economy, "Authorization & Billing", "gRPC/HTTP")
    Rel(platform, oracle, "Requests predictions", "Async Job")
    
    %% Inter-Service Logic
    Rel(scribe, engine, "Validates moves using", "Library Import")
    Rel(oracle, scribe, "Analyzes canonical games from", "Data Warehouse")
    
    %% Agent Interactions
    Rel(agents, platform, "Automates tasks via", "Public API")
    Rel(agents, economy, "Consumes credits for", "Compute")
```

# REST API

API reference for the Vindicta Platform.

> [!WARNING]
> **Provisional API**: The REST API is currently undergoing strict revision as part of the **Project Primordia** integration. The endpoints below are provisional. For stable interaction, use the [Vindicta-CLI](../getting-started/quickstart.md) or the Python SDKs directly.

---

## Base URL

```
https://api.vindicta.dev/v1  (Provisional Hosted)
http://localhost:8000/v1     (Local Orchestrator)
```

## Core Endpoints

### Evaluation (Project Primordia)

```http
POST /engine/evaluate
```

Submit a WARScribe transcript for analysis.

```json
{
  "transcript": "...",
  "config": {
    "edition": "10th",
<<<<<<< HEAD
=======
    "simulate_dice": true
>>>>>>> docs/migration-to-foundation
  }
}
```

### Oracle

```http
POST /oracle/ask
```

<<<<<<< HEAD
Query the Meta-Oracle for meta analysis or strategic advice.
=======
Query the Meta-Oracle for rules interpretations or strategic advice.
>>>>>>> docs/migration-to-foundation

---

## Error Responses

Standard HTTP status codes are used.

```json
{
  "status": 400,
  "error": "invalid_notation",
  "message": "Syntax error at line 4: Unknown unit 'SM-Tactical'"
}
```

## OpenAPI Spec

When running the unified platform via Docker, the full OpenAPI specification is available at:
`http://localhost:8000/docs`

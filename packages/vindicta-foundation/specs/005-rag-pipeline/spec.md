# Feature Specification: RAG Pipeline

**Feature Branch**: `005-rag-pipeline`  
**Created**: 2026-02-23  
**Status**: Draft  
**Input**: User description: "Implementation plan for RAG pipeline"

## Clarifications

### Session 2026-02-23

- Q: How should the scraper handle the different DOM structures of Wahapedia vs 40k.app? → A: Implement specific, dedicated extraction logic (selectors/parsers) for Wahapedia and 40k.app, falling back to a generic raw extraction if unmatched (Option A).
- Q: What should the system do when a scrape attempt fails (captcha, timeout, DOM change)? → A: Log the failure per-page, skip the failed page, and continue ingesting remaining pages (resilient mode with retry + logging) (Option B).
- Q: What level of observability should the MVP include? → A: Standard Python `logging` with structured log messages (timestamps, log levels, context) to stdout/file. No external observability tooling (Option A).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Local Agent Rules Retrieval (Priority: P1)

Agents within the Vindicta platform need to query rules reliably via a local tool server to provide accurate gameplay rulings and resolutions.

**Why this priority**: Without accurate and rapid retrieval of rules from the ecosystem, agents cannot reliably enforce the game system, making this the backbone of the interaction.

**Independent Test**: Can be fully tested by submitting a natural language search query to the RAG server client and receiving the exact relevant, accurate rules chunks from the stored data.

**Acceptance Scenarios**:

1. **Given** an agent running inside the platform, **When** it sends the query "What is the toughness of a Space Marine?", **Then** the local server successfully returns the most relevant rules chunks along with their version history from the database.

---

### User Story 2 - Automated Scraping and Data Ingest (Priority: P2)

As a platform maintainer, I want the system to ingest data from Wahapedia and 40k.app across their complex dynamic layouts, and store the most up-to-date chunks for AI retrieval, so that agents have the latest rules and errata.

**Why this priority**: Rule changes happen frequently. Stale rules make the agents unreliable, and manual data updates are unscalable.

**Independent Test**: Can be independently tested by running the scraper pipeline on a specific website snapshot and verifying the resultant text chunks are properly captured and uniquely identified.

**Acceptance Scenarios**:

1. **Given** a structural change or rules update on the target website, **When** the ingest pipeline runs, **Then** new rules segments are recognized, chunked, and stored alongside their unique metadata fingerprint.
2. **Given** an unchanged page, **When** the ingest pipeline runs, **Then** it ignores the duplicate content entirely, preventing stale or redundant storage.

### Edge Cases

- What happens when a website heavily alters its DOM structure, rendering the automated extraction rules invalid? → **Resolved**: The scraper logs the extraction failure for the affected page and continues processing remaining pages (FR-007).
- How does the system handle networking timeouts, rate limiting, or potential Cloudflare captchas from target websites? → **Resolved**: Per-page retry with structured logging; failed pages are skipped, and remaining pages continue ingesting (FR-007).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement dedicated extraction logic (CSS selectors/parsers) for each target site (Wahapedia, 40k.app), with a generic raw content extraction fallback for unrecognized sites.
- **FR-002**: System MUST convert the scraped web elements into clean markdown text that is optimized for consumption by Large Language Models.
- **FR-003**: System MUST identify the latest changes and only store unique, new text chunks using a cryptographic metadata hash (e.g. SHA-256).
- **FR-004**: System MUST store rule segments in a data structure intrinsically designed for embedding-based semantic AI retrieval.
- **FR-005**: System MUST serve search queries via the standard Model Context Protocol (MCP) server interface, making it universally accessible to compatible AI systems.
- **FR-006**: System MUST prioritize newly versioned rule chunks over outdated ones when returning retrieval results to inquiring agents.
- **FR-007**: System MUST handle scraping failures resiliently: log per-page failures with structured error details (URL, error type, timestamp), skip the failed page, and continue ingesting remaining pages without aborting the entire run.

### Non-Functional Requirements

- **NFR-001**: System MUST use Python's standard `logging` module with structured log messages (timestamps, log levels, contextual data) for all pipeline operations (scraping, storage, query serving). Logs MUST be emitted to stdout and optionally to a log file.

### Key Entities 

- **Rules Segment**: A contextual chunk of markdown rules text, accompanied by its embedding vector, URL origin, a unique hash, an insertion timestamp, and a version identifier so older versions of rules can be recognized.
- **Agent Query**: A focused natural language string passed to the server to look up rules.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Over 95% of agents' questions on basic unit statistics and abilities yield the correct excerpt in the top 3 retrieval results.
- **SC-002**: Search requests to the local server return contextual results in under 1.5 seconds under typical load.
- **SC-003**: The ingest system identifies unchanged content precisely, resulting in 0 duplicate entries being saved for unmodified pages.

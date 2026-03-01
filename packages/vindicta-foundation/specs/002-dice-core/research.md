# Research: dice-core

**Feature**: Dice Core — CSPRNG with Verifiable Entropy Proofs  
**Date**: 2026-02-22  
**Status**: Complete

---

## Research Topics

### Topic 1: CSPRNG in Python — `secrets` vs `os.urandom`

**Decision**: Use Python's `secrets` module as the primary CSPRNG interface.

**Rationale**:
- `secrets` is Python's stdlib module explicitly designed for cryptographic use cases (PEP 506).
- Internally delegates to `os.urandom()`, which sources from the OS kernel CSPRNG (`/dev/urandom` on Linux, `CryptGenRandom` on Windows).
- Provides `secrets.randbelow(n)` for unbiased integer generation within a range — no modular bias.
- FR-003 prohibits `random` module and `time.time()`; `secrets` satisfies this cleanly.
- No external dependency required — stdlib only.

**Alternatives Considered**:
| Alternative                                   | Rejected Because                                                                  |
| --------------------------------------------- | --------------------------------------------------------------------------------- |
| `os.urandom()` directly                       | Lower-level; would need to implement range clamping and bias elimination manually |
| `cryptography` library (`os.urandom` wrapper) | External dependency adds supply-chain surface for no benefit; stdlib suffices     |
| `pynacl` / `libsodium` bindings               | Heavy dependency for what is fundamentally `randbelow(n)`                         |
| Hardware RNG (`/dev/hwrng`)                   | Not portable; FR-005 requires pure Python API without hardware coupling           |

---

### Topic 2: Verifiable Entropy Proof Mechanism

**Decision**: Use HMAC-SHA256 commitment scheme with a reveal/verify protocol.

**Rationale**:
- Classic "commit-reveal" pattern: server commits to a seed hash **before** the roll, then reveals the seed **after** to prove the outcome was predetermined.
- HMAC-SHA256 provides both integrity and authentication — the server proves it used the committed seed without exposing the seed prematurely.
- Protocol:
  1. **Commit**: Generate seed `s`, compute `commitment = HMAC-SHA256(s, context)`, publish commitment.
  2. **Roll**: Derive result from `secrets.randbelow()` seeded deterministically from `s`.
  3. **Reveal**: Publish `s`. Auditor recomputes HMAC and the derived result to verify.
- `hashlib.sha256` and `hmac` are both stdlib — no external dependencies (FR-005).
- This directly satisfies FR-002 (cryptographic proof) and User Story 2 (external auditor verification).

**Alternatives Considered**:
| Alternative                        | Rejected Because                                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Simple SHA-256 hash of seed        | No authentication — vulnerable to length-extension attacks; HMAC is strictly superior                   |
| Digital signatures (e.g., Ed25519) | Requires key management, external libraries (`cryptography`/`pynacl`); overkill for single-server proof |
| Zero-knowledge proofs              | Enormous complexity for a dice engine; not justified by requirements                                    |
| Hash chains (blockchain-style)     | Adds statefulness and chain management; unnecessary for per-roll proofs                                 |

---

### Topic 3: Deterministic Seeding for Test Environments

**Decision**: Provide an explicit `DeterministicRng` adapter gated behind an environment variable + runtime mode enum.

**Rationale**:
- FR-004 requires deterministic seeding for CI/testing but prohibits it in production.
- Strategy: define a `RngMode` enum (`PRODUCTION`, `TESTING`) and a factory function that returns either the real CSPRNG engine or a deterministic test double.
- The deterministic adapter uses Python's `random.Random(seed)` (non-crypto) explicitly labeled and gated.
- Runtime guard: `if mode == PRODUCTION and seed is not None: raise SecurityError`.
- This provides repeatable tests without compromising production integrity.

**Alternatives Considered**:
| Alternative                        | Rejected Because                                                            |
| ---------------------------------- | --------------------------------------------------------------------------- |
| Monkey-patching `secrets` in tests | Fragile, non-portable, and violates the principle of explicit configuration |
| `PYTHONHASHSEED` env variable      | Only affects hash randomization, not `secrets`/`os.urandom`                 |
| Compile-time flag                  | Python doesn't have compile-time flags; runtime enum is idiomatic           |

---

### Topic 4: Performance Target — Sub-Millisecond Roll Generation

**Decision**: Achievable with stdlib only; no performance-specific optimizations needed.

**Rationale**:
- SC-003 requires < 1ms per roll+proof generation.
- Benchmarks of `secrets.randbelow(6)` consistently show ~1-5 μs per call on modern hardware.
- HMAC-SHA256 computation for a 32-byte seed: ~2-5 μs.
- Combined: well under 100 μs per roll, far below the 1ms target.
- No need for caching, pre-computation, or async — synchronous stdlib calls suffice.

**Alternatives Considered**:
| Alternative                  | Rejected Because                                                  |
| ---------------------------- | ----------------------------------------------------------------- |
| Pre-generating entropy pools | Adds statefulness and complexity for no gain against a 1ms budget |
| C extension for HMAC         | stdlib `hmac` module already uses OpenSSL C bindings internally   |
| Batch roll generation        | Premature optimization; single-roll path is already sub-100μs     |

---

### Topic 5: Statistical Validation — Dieharder / NIST SP 800-22

**Decision**: Validate via chi-square uniformity test in CI; defer full Dieharder suite to SC-001 success criteria verification.

**Rationale**:
- SC-001 requires passing standard statistical suites with >99% confidence.
- Python's `secrets.randbelow()` inherits OS CSPRNG quality — it will pass Dieharder by definition.
- For CI, a chi-square goodness-of-fit test over 100k samples is sufficient to catch integration regressions.
- Full Dieharder run is a one-time validation activity, not a per-commit CI step.

**Alternatives Considered**:
| Alternative                         | Rejected Because                                                                                |
| ----------------------------------- | ----------------------------------------------------------------------------------------------- |
| Running full Dieharder in CI        | Takes minutes; not appropriate for per-commit testing                                           |
| Skipping statistical tests entirely | Would leave SC-001 unverified                                                                   |
| Using NIST SP 800-22 test suite     | Requires C compilation (`sts`); overkill for wrapping an OS CSPRNG. Reserve for one-time audit. |

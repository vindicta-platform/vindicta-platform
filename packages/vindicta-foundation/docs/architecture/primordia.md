# Project Primordia: The Warhammer 40,000 Evaluation Engine

> "The future of Warhammer 40,000 is not just in the hands of the players, but in the silicon of the evaluation engine that can truly see the war for the empires it builds."

## 1. Core Philosophy

To build an engine capable of rivaling Stockfish/AlphaZero by abstracting the Warhammer 40k battlefield into a finite, massive mathematical state space. The goal is moving from "feel" to "deterministic fact."

## 2. State Space & Complexity

- **Battlefield**: 44" x 60" continuous surface.
- **Discretization**: 0.1" resolution -> ~264,000 cells ($440 \times 600$).
- **State Complexity**: $>10^{250}$ (exceeds Go and Chess).
- **Approach**: Multi-layered renormalization (High-res objectives, Low-res open space).

## 3. High-Performance State Representation

### Hierarchical Bitboards

- **Master Bitboard**: Tracks active zones.
- **Zone Bitboards**: 64-bit words representing local spatial data.
- **Operations**: SMID/AVX-512 optimized bitwise AND/OR/XOR for LoS, Auras, and Range checks.
- **Magic Bitboards**: Precomputed movement and visibility paths.

### Zobrist Hashing

- **Purpose**: $O(1)$ state retrieval from Transposition Tables.
- **Hash Components**:
  - Unit Positions
  - Unit Health (unique string for every wound state of every model)
  - Resources (CP, Stratagems)
  - Global Buffs
  - Phase & Active Player

## 4. Evaluation Function (20-0 Scale)

### Metrics

- **Mathhammer (Material)**:
  - **OV (Offensive Value)**: Expected damage vs GEQ/MEQ/TEQ.
  - **DV (Defensive Value)**: Effective wounds (T, Sv, Invuln, FNP).
- **Positional**:
  - **OC Efficiency**: Holding objectives.
  - **Screen Integrity**: Denying enemy movement.
  - **Tempo**: Forcing opponent reactions.
- **Neural Evaluation (NNUE)**:
  - Learned weights from millions of simulated/tournament games.
  - Concepts evaluated: "Who's the Beatdown?", Trap Detection.

### Handling Stochasticity

- **Probability Convolution**: Modeling dice results as PMFs (Probability Mass Functions), not averages.
- **Risk Adjustment**: Discounting evaluation based on variance (Gaussian approx for volume fire).
- **Chance Nodes**: Implementing Expectiminimax or MCTS chance nodes.

## 5. Search Strategy

- **Quiescence Search**: Resolving "Noisy" positions (Engagement Range, Overwatch, Battleshock) before static eval.
- **Endgame Tablebases**:
  - Detect "Point Lock" (Mate).
  - Condition: $VP_{lead} > VP_{max\_possible\_enemy}$.

## 6. Output & Telemetry

- **Protocol**: UCI (Universal Chess Interface).
- **UI**: Real-time Advantage Meter (Centipawns -> 20-0 WTC Scale).
- **Broadcast**: AR compatibility via Event Stream (Kafka).

## 7. Implementation Roadmap

1. **Phase 1: Combat Patrol**: Smaller state space, fixed lists.
2. **Phase 2: Strike Force**: Full 2000pt scaling, Hybrid MCTS/Alpha-Beta.
3. **Phase 3: Strategic Engineering**: Rule/Point simulation for balance testing.

## 8. Hardware Specs

- **CPU**: SIMD / AVX-512 support.
- **GPU**: NVIDIA Blackwell / RTX for NNUE.
- **RAM**: Fast MRAM for Transposition Tables.

# The Inference Layer Specification

**Function:** Conversion of WARScribe Strings to Deterministic State Hashes
**Logic:** Bridge between the Manifestation (UI) and the Engine (Search)

The Inference Layer is the "Translator" of the system. It takes the human-readable **WARScribe** log and converts it into a 64-bit **Zobrist Hash** that the **Primordia Engine** uses for its search tree.

## I. The BSH (Board State Hash) Generator

The Inference Layer monitors the **WARScribe** stream and maintains a "Running State." When a move or attack occurs, the generator updates the **Board State Hash (BSH)**.

**The Zobrist Hashing Process:**

1. **Initialize Table:** A large table of random 64-bit integers is created for every possible unit state (Position, Health, Active Buffs).
2. **XOR Operation:** To update the state, the engine performs a bitwise XOR. If Unit 1 moves from Pos A to Pos B, the engine XORs the "Unit 1 at A" value (removing it) and then XORs the "Unit 1 at B" value (adding it).
3. **Result:** A single 64-bit integer represents the entire 2,000-point game state.

## II. The Formation "Hydrator" (MGF Component)

Because WARScribe uses **Centroid Anchoring**, the Inference Layer must "Hydrate" the unit—calculating exactly where every individual model is located to perform **Collision Checks** and **Line of Sight**.

**The Hydration Algorithm:**

- **Step 1:** Retrieve the `Centroid` and `Formation_Tag` from the BSH.
- **Step 2:** Look up the `Formation_Logic` in the **Vindicta Constitution Library**.
- **Step 3:** Generate a local coordinate list for $M$ models based on base size (e.g., 32mm).
- **Step 4:** Run the **Axiom of Unity** check to ensure no models are overlapping terrain or enemy units.

## III. The Probability Resolver (Chance Node Mapping)

When WARScribe records an interaction like an attack, the Inference Layer maps the results into the engine's **Transposition Table**.

- **Input:** `U1 A U2 (!H3 ?W1)`
- **Translation:** The engine notes that the "Standard Distribution" (Mean) was bypassed by the actual result. It updates the **Advantage Meter** based on the *actual* damage dealt, but keeps the *expected* damage in its look-ahead memory for Turn 4 and 5 projections.

## IV. Data Integrity: The Sync-Check

To prevent "Desync" between the table and the software, the Inference Layer performs a **Checksum** every Turn.

> **Protocol:** If the **WARScribe** Centroid differs from the **Logi-Slate** UI representation by more than 0.1", the Inference Layer triggers a "State Correction" and re-hydrates the unit based on the last known-good WARScribe entry.

# Toward WARScribe: A Rigorous Synthesis of Formal Notation Systems and Game Description Languages for Tabletop Wargaming

The creation of a universal, rigorous wargaming notation system, designated here as WARScribe, requires a departure from the fragmented and informal shorthand systems that currently permeate the tabletop hobby. For decades, players of complex wargames such as Warhammer 40,000 have relied on ad hoc methods for recording game states, ranging from scribbled notes in margins to digital lists that lack temporal coherence. To establish a notation that is truly language-agnostic and edition-independent, it is necessary to synthesize the formal logic of game description languages (GDL) with the spatial precision of coordinate reference systems and the proven efficiency of established competitive notations. This report explores the multidisciplinary foundations required for such a system, addressing the critical issues of unit identity, combat resolution, and modification logic.

## The Evolution of Formal Game Notations: Historical Precedents

The development of WARScribe must be contextualized within the history of competitive game recording, where the move from narrative description to symbolic shorthand has always marked the professionalization of a discipline. Early chess literature, for instance, relied on lengthy prose to describe each move, which was prone to error and inhibited the preservation of strategic analysis. The transition to Algebraic Chess Notation (ACN) in the 18th century, popularized by Philip Stamma, revolutionized the field by assigning a unique coordinate (a–h for files, 1–8 for ranks) to every square.

### Comparative Mechanics of Traditional Notations

| System                             | Foundation               | Scope                 | Primary Advantage                                       |
| :--------------------------------- | :----------------------- | :-------------------- | :------------------------------------------------------ |
| **Algebraic Chess Notation (ACN)** | 8x8 Cartesian Grid       | Move sequences        | Minimal redundancy and language-agnostic symbols.       |
| **Portable Game Notation (PGN)**   | ASCII-based Text         | Complete game history | Human-readable and machine-parsable.                    |
| **Forsyth–Edwards Notation (FEN)** | Character String         | Static board snapshot | Captures current state in a single line.                |
| **Go Shorthand**                   | 19x19 Grid Intersections | Strategic placement   | Uses symbols (triangles, circles) for grouped analysis. |
| **Music Shorthand**                | Relative Intervals       | Pitch and Rhythm      | "Jump Rule" manages relative shifts between notes.      |

In chess, the evolution from Descriptive Notation (e.g., "P-K4") to Standard Algebraic Notation (e.g., "e4") demonstrates the value of suppressing machine-redundant information. SAN only specifies the origin square if multiple pieces of the same type can reach the same destination, using the file or rank as a discriminator (e.g., Nge2). For WARScribe, this principle of "disambiguation via origin" is essential for resolving the Identity Problem in mass-combat systems.

Go notation provides a different perspective, emphasizing the semantic categorization of intersections. Terms such as hoshi (star points) and tengen (origin of heaven) provide fixed references on a larger grid. Furthermore, Go diagrams frequently use symbols like triangles, squares, and circles to denote subsets of stones for strategic discussion, a method that WARScribe could adapt to mark models affected by specific area-of-effect (aura) abilities.

Musical notation offers a vital lesson in relative versus absolute pitch. Eastern neumes are "differential," indicating whether a pitch rises or falls relative to the previous step rather than its absolute frequency. Shorthand musical notation utilizes a "Jump Rule" where a melody that increases by a perfect fourth or more is placed on an elevated line, remaining there until it descends, at which point it returns to the neutral line. This logic is directly applicable to 3D wargaming movement, where recording a displacement vector relative to the previous position is often more practical than maintaining global coordinates for every model.

## Computational Foundations: Game Description Languages

Beyond simple shorthand, WARScribe must function as a formal language capable of describing the intricacies of game rules and dynamics to artificial intelligence. Stanford’s Game Description Language (GDL) serves as the primary model for this approach. GDL is a logic-based language designed for General Game Playing (GGP), allowing AI agents to understand games they have never played before by processing a set of declarative rules.

### The GDL State Machine Architecture

GDL models a game as a finite state machine where every state is defined by a set of true propositions. The transition function—the rules of the game—defines what is true in the next state based on the current state and the collective moves of the players.

| GDL Keyword | Logical Function          | WARScribe Mapping                                               |
| :---------- | :------------------------ | :-------------------------------------------------------------- |
| `role`      | Defines player identities | Attacker, Defender, Neutral.                                    |
| `init`      | Sets the initial state    | Deployment zones and army lists.                                |
| `legal`     | Determines valid actions  | Phase-restricted move or attack eligibility.                    |
| `does`      | Records player choices    | Specific dice rolls or model repositioning.                     |
| `next`      | State update function     | Resultant model removals or state changes (e.g., Battle-shock). |
| `terminal`  | Completion criteria       | Mission-specific ending conditions (e.g., Turn 5).              |

Standard GDL is limited to deterministic, perfect-information games, but its extension, GDL-II, introduces the `sees` and `random` keywords to handle incomplete information and elements of chance. This is critical for wargames, where the outcome of an attack is determined by a stochastic dice pipeline. Ludii (L-GDL) further optimizes this by modeling games as structured trees of "ludemes"—basic units of game information. In L-GDL, the equipment (board, pieces, dice) and rules are parsed as a hierarchy, which allows for highly efficient game simulations. WARScribe can leverage this tree-like structure to resolve the Modification Problem, treating stratagems and auras as modifier nodes that attach to specific branches of the resolution tree.

## The Partake Language and Situational Duality

Partake introduces a critical duality between situations and actors, focusing on how entities accrue attributes over time. Unlike traditional object-oriented systems that require fixed structures, Partake uses a relational model where game objects are symbolic entities defined by tuples of facts (e.g., health P -> 10). This provides a direct solution to the Identity Problem. A model in WARScribe is not a static object but a symbolic ID that gains salience through its relationships to its unit, its datasheet, its current health, and the transient effects acting upon it.

Partake also utilizes deictic predicates—indexical terms like "the current turn" or "the model designated as the target"—which simplify rule encoding by focusing on the narrative moment. This "linguistic indexicality" allows WARScribe to record complex sequences like "the current unit piles in toward the closest enemy" without needing to resolve every coordinate until the final state is captured.

## Tabletop Specifics: Coordinate Systems and State Capture

Wargaming occurs in a continuous 3D space, making standard Cartesian grids insufficient. The mapping of this space requires a Compound Coordinate Reference System (CCRS), integrating horizontal and vertical geodetic datums. For game engines like Unity and Unreal, the orientation of these axes matters significantly, as they adopt either left-hand or right-hand coordinate systems.

### Relative Vector Notation (RVN)

In physical wargaming, recording the absolute position of a model $(x, y, z)$ is tedious and subject to measurement drift. WARScribe should instead prioritize Relative Vector Notation. Based on the physics of displacement, the vector $\vec{d}$ represents the change in position between two points $P_1$ and $P_2$.

The magnitude of displacement is calculated via the Pythagorean theorem:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$$

In WARScribe shorthand, a move is recorded as a displacement vector relative to the starting position:

```
MOV:UID1 {5.5", 135°, +1"}
```

This indicates that UID1 moved 5.5 inches at a 135-degree angle with a vertical gain of 1 inch. This notation is resilient because the displacement vector remains the same regardless of the choice of origin on the table.

### Digital State Capture and Tournament Data

Digital platforms provide existing schemas for state capture. Tabletop Simulator (TTS) uses JSON serialization for save files, recording every object's unique GUID, its physics properties (friction, bounciness), and its transform state (position, rotation, scale). BCP (Best Coast Pairings) focuses on tournament-level data, including player rankings, placings, and structured army lists. BCP uses a JSON:API standard that organizes data into resources and operations, which WARScribe must align with to facilitate data interchange.

## Solving the Identity Problem: Unique Model Identification

The Identity Problem arises from the need to distinguish between multiple identical models within a single unit. In Warhammer 40,000, identifying "the third model in a squad of ten" is vital for tracking casualties and aura ranges.

### The Semantic ID Hierarchy

WARScribe addresses this through a hierarchical, semantic ID system:

1. **Unit Identifier (UID):** A unique tag for the unit based on its role and sequence (e.g., `TRP1` for the first Troop unit).
2. **Model Index (MID):** A sequence number within the unit (e.g., `TRP1.4`).
3. **Role/Gear Suffix (RGS):** Denotes special equipment or status (e.g., `TRP1.4[Melta]`).

This mirrors the structured data in TTS save files, where lists of snap points and vector lines are attached to specific objects. By using semantic IDs instead of raw GUIDs, WARScribe remains human-readable while providing the precision needed to track combat resolution at the individual model level.

## The Resolution Problem: Encoding the Stochastic Pipeline

The Resolution Problem involves condensing the multi-step process of wargaming combat—Hit, Wound, Save, Damage (H-W-S-D)—into a compact and reversible string. Standard resolution in Warhammer 40,000 involves rolling to hit based on Ballistic Skill (BS), rolling to wound based on Strength (S) versus Toughness (T), and the target rolling to save based on armor or invulnerable saves.

### The Combat Resolution String

A WARScribe resolution string for a single attack would look as follows:

```
(UID1.4 -> UID2) {H5, W6, S1*X, D2}
```

- **H5:** Hit roll result of 5 (Success).
- **W6:** Wound roll result of 6 (Critical Wound).
- **S1*X:** Save roll result of 1 (Failure), with X denoting the destruction of the model.
- **D2:** 2 points of damage applied.

This draws heavily from the BattleTech "GATOR" system, which provides a standardized checklist for calculating to-hit modifiers: Gunner Skill, Attacker Movement, Target Movement, Other, and Range. By encoding the modifiers and the raw dice result, the notation becomes reversible and edition-independent.

### Fast Rolling and Individual Resolution

While wargamers often "fast roll" dice for convenience, 40k technically resolves every attack individually. WARScribe must maintain this individual logic. If a unit is damaged, every instance of damage must be applied separately to the same model until it is removed, at which point the next model is selected. WARScribe captures this sequentiality through its string-based resolution, ensuring that spillover damage or "feel no pain" (FNP) rolls are correctly accounted for model-by-model.

## The Modification Problem: Auras, Stratagems, and Temporary Effects

Tabletop wargames are defined by dynamic modifiers that shift the probabilities of the stochastic pipeline. Auras (area-of-effect buffs) and Stratagems (reactive abilities) create complex interactions that WARScribe must track.

### Aura Wrapping and Temporal Logic

Using the Partake model, an aura is not a change to a unit's base datasheet but a situational rule that matches a specific condition. WARScribe handles this via "Aura Wrapping." A unit in proximity to a leader is tagged in the resolution string:

```
ATK:(UID1 @AUR:Captain) -> TGT:UID2
```

This indicates that UID1 is attacking while under the influence of the Captain's aura, which might allow for re-rolls of 1s to hit.

### Stratagems as Interrupts

Stratagems like "Overwatch" or "Heroic Intervention" function as temporal interrupts. In 10th edition, the Overwatch stratagem can be triggered during the opponent's movement or charge phase. WARScribe records this as a non-linear branch in the turn sequence:

```
 -> -> (ATK:UID2 -> UID1)
```

This preserves the causal relationship between the movement of the first unit and the reactive fire of the second.

## Edition Mapping: Resilience Across Rule Shifts

A primary goal of WARScribe is to remain functional as game systems evolve. Analyzing the transition from 9th to 10th edition Warhammer 40,000 illustrates the required resilience.

### Mapping Edition Changes

| Mechanic        | 9th Edition                      | 10th Edition                       | WARScribe Adaptation                         |
| :-------------- | :------------------------------- | :--------------------------------- | :------------------------------------------- |
| **Morale**      | Combat Attrition (Model removal) | Battle-shock (OC 0, No Stratagems) | Record state `` on Unit ID.                  |
| **Fight Order** | Fight First / Normal / Last      | Fight First / Normal (Simplified)  | Use priority tags `P1`, `P2`.                |
| **Movement**    | Ignore vertical (Fly)            | Fly requires diagonal measurement  | RVN vector (r, θ, h) accounts for height.    |
| **Leadership**  | Roll equal/under                 | Roll equal/over                    | Record raw result to maintain reversibility. |

The move from 9th to 10th edition saw the removal of the "Fight Last" sub-phase. In WARScribe, the use of priority tags (P1 for Fight First, P2 for Fight Normal) allows the notation to survive this change; the rules of the current edition determine which units receive which tags, but the notation itself remains consistent. Similarly, the change in Leadership logic (Higher is now better) is handled by recording the raw dice result and the target characteristic, allowing the resolution to be parsed correctly regardless of the prevailing edition’s math.

### Detailed Analysis of Edition Mapping: 9th, 10th, and 11th

The transition between 9th and 10th edition Warhammer 40,000 provides a case study in how notation must adapt to evolving rulesets. One of the most significant changes occurred in the Charge and Fight phases. In 9th edition, the fight phase was divided into three distinct steps: Fight First, Fight Normal, and Fight Last. This required a complex three-tier priority system. 10th edition eliminated the "Fight Last" tier, simplifying the process into a two-tier system where units alternate starting with the player whose turn is not taking place.

WARScribe handles this by using ordinal priority markers. Instead of hard-coding "Fight First," the notation uses `[P1]`, `[P2]`, and `[P3]`. In 10th edition, `[P3]` simply remains unused unless a specific mission rule or future edition re-introduces a third tier of priority. This allows the notation to remain stable while the game balance shifts.

Another critical change was the introduction of Battle-shock to replace the older Morale system. In 9th edition, failing a Morale test led to the direct removal of models through Combat Attrition. In 10th edition, failure results in the Battle-shocked state, which sets Objective Control (OC) to 0 and prevents the use of Stratagems. WARScribe records this not as "a morale failure" but as a state transition on the unit ID:

```
UID1{Ld_Test} -> Result:Fail -> UID1
```

This records the event (the test), the outcome (the failure), and the consequent state (Battle-shocked). Because the notation records the state rather than the specific penalty, it remains accurate even if the effects of Battle-shock are modified in 11th edition.

## Technical Breakdown: Tabletop Simulator JSON Structure

The state capture capabilities of Tabletop Simulator (TTS) offer a blueprint for the "Expanded WARScribe" (EWS) format. TTS save files are human-readable JSON that categorize data into specific serialized classes.

### Serialized Classes in TTS Save Files

| Class                    | Properties Captured                         | WARScribe Integration                                |
| :----------------------- | :------------------------------------------ | :--------------------------------------------------- |
| **SaveState**            | SaveName, GameMode, Gravity, PlayArea       | Mission metadata and table settings.                 |
| **PhysicsMaterialState** | DynamicFriction, StaticFriction, Bounciness | Environmental factors and terrain effects.           |
| **TransformState**       | Position, Rotation, Scale                   | The physical grounding for Relative Vector Notation. |
| **SnapPointState**       | AttachedVectorLines, GUID                   | Tracks model coherency and engagement range.         |

A key feature of TTS is the `onObjectPickUp` and `onObjectDrop` event handlers. These events allow a scripting engine to record movement vectors in real-time. WARScribe can utilize these triggers to automatically generate move strings:

```
onObjectDrop(player, object) -> CalcVector(start, end) -> WriteCWS("MOV:UID")
```

This digital-first approach ensures that the notation is a true representation of the physical state of the board.

## The Resolution of the Modification Problem in BattleTech

The "Modification Problem" in wargaming often relates to how movement and shooting are adjusted by terrain and situational factors. BattleTech provides a rigorous precedent for this with the PSR (Piloting Skill Roll) and GATOR systems.

### The GATOR Algorithm for Attack Declaration

In BattleTech, the target number for an attack is built sequentially:

1. **G (Gunnery):** The base skill of the pilot.
2. **A (Attacker):** Modifiers based on whether the attacker walked, ran, or jumped.
3. **T (Target):** Modifiers based on the target's movement distance.
4. **O (Other):** Modifiers for heat, damage, or specific gear.
5. **R (Range):** Short, Medium, or Long distance penalties.

WARScribe adopts this checklist approach for its resolution strings. Instead of just recording the final "hit," the notation includes the base BS and the stack of modifiers:

```
UID1.4 -> UID2 {BS3+, MOD:+1(Heavy), MOD:-1(Cover)} -> Result:4(Pass)
```

By recording the factors (Heavy weapon bonus, Cover penalty), the notation provides a complete record of the "Modification" at the moment of resolution, making it easy to spot errors or analyze strategic choices in post-game reviews.

## Advanced Coordinate Reference Systems (CRS)

Wargaming movement often involves complex interactions with terrain features. Relative Vector Notation is most effective when anchored in a robust CRS. Game developers differentiate between Cartesian systems based on their orientation. Unreal Engine, for example, assigns the XYZ axes to Forward, Right, and Up, while Unity uses Right, Up, and Forward.

For WARScribe to be truly universal, it must define a standard orientation for its Cartesian basis:

- **X-axis:** The horizontal width of the table (East-West).
- **Y-axis:** The vertical height (Elevation).
- **Z-axis:** The horizontal depth of the table (North-South).

This right-handed coordinate system allows for the use of standard rotation matrices to resolve model pivots and aircraft movements. In 10th edition, aircraft movement became more restricted, with models no longer able to pivot before moving unless they are in Hover mode. WARScribe records these pivots as angular displacements:

```
ROT:UID1 {Pivot: 90°}
```

Combined with RVN, this provides a mathematically complete record of any model's path through 3D space.

## Conclusion and Future Directions

WARScribe represents a convergence of several disparate fields: the efficiency of chess notation, the logic of GDL, the relational semantics of Partake, and the physical state capture of digital tools like Tabletop Simulator. By addressing the Identity, Resolution, and Modification problems through a rigorous, symbolic grammar, WARScribe provides the first truly universal language for the tabletop wargaming community.

Future development will focus on the automation of this notation through computer vision and digital overlays. As players increasingly turn to virtual tabletop environments and augmented reality aids, the demand for a machine-parsable, edition-independent record of play will only grow. WARScribe is the foundational step toward that future, providing a language that is as durable as the hobby it serves.

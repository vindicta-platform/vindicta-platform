# Examples

Hello World scripts demonstrating key Vindicta Platform APIs.

## 🎲 dice_roll.py

Rolls dice using the cryptographically secure `DiceEngine`. Demonstrates:
- Single D6 rolls with entropy proofs
- Batch rolls (10D6) with statistics
- The audit trail that makes every roll verifiable

```bash
uv run examples/dice_roll.py
```

## 📜 warscribe_actions.py

Creates game actions using the WARScribe notation schema. Demonstrates:
- Unit references for battlefield entities
- Movement, shooting, and charge actions
- JSON serialization of the complete action log

```bash
uv run examples/warscribe_actions.py
```

## ⚔️ combat_sim.py

End-to-end combat simulation combining the Dice Engine with WARScribe actions. Demonstrates:
- Creating units and weapons
- Running a full hit → wound → save → damage sequence
- Recording the result as a structured `ShootAction`
- Printing the complete combat transcript

```bash
uv run examples/combat_sim.py
```

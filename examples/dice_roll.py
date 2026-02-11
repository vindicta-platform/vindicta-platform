#!/usr/bin/env python3
"""Hello World: Dice Engine.

Demonstrates rolling dice with cryptographic entropy proofs
using the Vindicta Platform's DiceEngine.
"""

from vindicta_engine.physics.engine import DiceEngine


def main() -> None:
    print("⚔️  Vindicta Platform — Dice Engine Demo")
    print("=" * 45)

    engine = DiceEngine()

    # --- Single roll ---
    print("\n🎲 Single D6 Roll")
    roll = engine.roll_d6()
    print(f"   Result : {roll.value}")
    print(f"   Proof  : {roll.entropy_proof}")

    # --- Batch roll ---
    print("\n🎲 Batch Roll: 10D6")
    batch = engine.roll_batch(count=10, sides=6)
    print(f"   Values  : {batch.values}")
    print(f"   Total   : {batch.total}")
    print(f"   Average : {batch.average:.1f}")

    # --- Entropy audit trail ---
    print("\n🔐 Entropy Proofs (audit trail)")
    for i, r in enumerate(batch.rolls, 1):
        print(f"   Roll {i:2d}: D{r.sides} = {r.value}  proof={r.entropy_proof}")

    print("\n✅ Every roll is CSPRNG-backed and independently verifiable.")


if __name__ == "__main__":
    main()

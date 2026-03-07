#!/usr/bin/env python3
"""Hello World: Full Combat Simulation.

Combines the Dice Engine with WARScribe actions to simulate
a complete shooting attack and record it as a structured action.
"""

import json

from vindicta_engine.physics.engine import DiceEngine
from warscribe.core.schema.unit import UnitReference
from warscribe.core.schema.action import ActionResult, ShootAction


def main() -> None:
    print("⚔️  Vindicta Platform — Combat Simulation Demo")
    print("=" * 50)

    # --- Setup ---
    engine = DiceEngine()

    attacker = UnitReference(
        name="Hellblaster Squad",
        faction="Ultramarines",
        models_remaining=5,
<<<<<<< HEAD
        wounds_remaining=10,
        position_x=0.0,
        position_y=0.0,
=======
>>>>>>> origin/chore/langfuse-integration
    )
    target = UnitReference(
        name="Plague Marines",
        faction="Death Guard",
        models_remaining=5,
<<<<<<< HEAD
        wounds_remaining=10,
        position_x=12.0,
        position_y=0.0,
    )

    print(f"\n⚔️  {attacker} vs {target}")
    print("   Weapon: Plasma Incinerator (supercharge)")
    print("   Profile: 5 attacks, BS 3+, S8 vs T5 (wound 3+), Sv 3+, D2")
=======
    )

    print(f"\n⚔️  {attacker} vs {target}")
    print(f"   Weapon: Plasma Incinerator (supercharge)")
    print(f"   Profile: 5 attacks, BS 3+, S8 vs T5 (wound 3+), Sv 3+, D2")
>>>>>>> origin/chore/langfuse-integration

    # --- Simulate combat with the engine ---
    combat = engine.combat_roll(
        attacks=5,
        hit_on=3,
        wound_on=3,
        save=3,
        damage=2,
    )

<<<<<<< HEAD
    print("\n🎲 Dice Results")
=======
    print(f"\n🎲 Dice Results")
>>>>>>> origin/chore/langfuse-integration
    print(f"   Hit rolls  : {[r.value for r in combat.hit_rolls]}")
    print(f"   Hits        : {combat.hits}/{combat.attacks}")
    print(f"   Wound rolls : {[r.value for r in combat.wound_rolls]}")
    print(f"   Wounds      : {combat.wounds}/{combat.hits}")
    print(f"   Save rolls  : {[r.value for r in combat.save_rolls]}")
    print(f"   Failed saves: {combat.saves_failed}/{combat.wounds}")
    print(f"   Damage dealt: {combat.damage_dealt}")

    # --- Record as a WARScribe action ---
    models_killed = combat.damage_dealt // 2  # 2 wounds per Plague Marine

    action = ShootAction(
        turn=1,
        phase="shooting",
        actor=attacker,
        target=target,
        weapon_name="Plasma Incinerator (supercharge)",
        shots=combat.attacks,
        hits=combat.hits,
        wounds=combat.wounds,
        saves_failed=combat.saves_failed,
        damage_dealt=combat.damage_dealt,
        models_killed=models_killed,
        result=ActionResult.SUCCESS if combat.damage_dealt > 0 else ActionResult.FAILED,
<<<<<<< HEAD
        notes="Simulation of Plasma Incinerator",
    )

    print("\n📜 Combat Transcript")
    print(f"   {action.actor.name} fires {action.weapon_name} at {action.target.name}")
=======
    )

    print(f"\n📜 Combat Transcript")
    print(
        f"   {action.actor.name} fires {action.weapon_name} at {action.target.name}"
    )
>>>>>>> origin/chore/langfuse-integration
    print(
        f"   Result: {action.shots}S → {action.hits}H → {action.wounds}W → "
        f"{action.damage_dealt}D ({models_killed} models killed)"
    )

    # --- Full JSON output ---
    print("\n📄 Full Action JSON:")
    print(json.dumps(json.loads(action.model_dump_json()), indent=2))

    # --- Entropy verification ---
    print("\n🔐 Entropy Proofs (hit rolls)")
    for i, roll in enumerate(combat.hit_rolls, 1):
        print(f"   Roll {i}: D{roll.sides} = {roll.value}  proof={roll.entropy_proof}")

    print("\n✅ Combat fully simulated with auditable dice and structured notation.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Hello World: WARScribe Action Notation.

Demonstrates creating and serializing game actions
using the WARScribe notation schema.
"""

import json

from warscribe.core.schema.unit import UnitReference
from warscribe.core.schema.action import (
    ActionResult,
    MoveAction,
    ShootAction,
    ChargeAction,
)


def main() -> None:
    print("⚔️  Vindicta Platform — WARScribe Action Notation Demo")
    print("=" * 55)

    # --- Create units ---
    intercessors = UnitReference(
        name="Intercessor Squad Alpha",
        faction="Ultramarines",
        models_remaining=5,
    )
    warriors = UnitReference(
        name="Necron Warriors",
        faction="Necrons",
        models_remaining=10,
    )

    print(f"\n📋 Units: {intercessors} vs {warriors}")

    # --- Movement ---
    move = MoveAction(
        turn=1,
        phase="movement",
        actor=intercessors,
        distance_inches=6.0,
        result=ActionResult.SUCCESS,
    )
    print(f'\n🏃 Move: {intercessors.name} advances {move.distance_inches}"')

    # --- Shooting ---
    shoot = ShootAction(
        turn=1,
        phase="shooting",
        actor=intercessors,
        target=warriors,
        weapon_name="Bolt Rifle",
        shots=10,
        hits=7,
        wounds=4,
        saves_failed=3,
        damage_dealt=3,
        models_killed=3,
        result=ActionResult.SUCCESS,
    )
    print(
        f"🔫 Shoot: {shoot.weapon_name} — "
        f"{shoot.shots}S → {shoot.hits}H → {shoot.wounds}W → "
        f"{shoot.damage_dealt}D ({shoot.models_killed} killed)"
    )

    # --- Charge ---
    charge = ChargeAction(
        turn=1,
        phase="charge",
        actor=intercessors,
        targets=[warriors],
        charge_roll=(4, 3),
        distance_needed=6.5,
        made_charge=True,
        result=ActionResult.SUCCESS,
    )
    print(
        f'⚡ Charge: roll {charge.charge_roll} = {sum(charge.charge_roll)}" '
        f'(needed {charge.distance_needed}") — '
        f"{'Made it!' if charge.made_charge else 'Failed!'}"
    )

    # --- Serialize ---
    print("\n📄 Action Log (JSON)")
    actions = [move, shoot, charge]
    for action in actions:
        data = json.loads(action.model_dump_json())
        print(f"  {data['action_type']:10s} | turn {data['turn']} | {data['phase']}")

    # Full JSON of the shoot action
    print("\n📜 Full ShootAction JSON:")
    print(json.dumps(json.loads(shoot.model_dump_json()), indent=2))


if __name__ == "__main__":
    main()

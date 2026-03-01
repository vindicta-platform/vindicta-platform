from enum import IntEnum
from dataclasses import dataclass

from vindicta_economy.ledger.manager import VoidBankerManager


class PriorityLevel(IntEnum):
    BACKGROUND_SIMULATION = 0
    STANDARD_OPERATION = 1
    LIVE_GAME_STATE = 2
    SYSTEM_CRITICAL = 3


class ResourceExhaustionHalt(Exception):
    """Raised when the system enters a critical resource state."""

    pass


@dataclass
class PolicyConfig:
    thermal_limit_celsius: float = 85.0
    load_shedding_threshold: float = 0.90  # 90% CPU/GPU load
    min_solvency_buffer: float = 10.0  # Minimum credits required to operate


class ResourcePolicy:
    def __init__(
        self, manager: VoidBankerManager, config: PolicyConfig = PolicyConfig()
    ):
        self.manager = manager
        self.config = config

    async def enforce_policy(
        self, agent_id: str, priority: PriorityLevel, estimated_cost: float
    ):
        """
        Enforce resource policy before allowing an operation.
        Raises ResourceExhaustionHalt if the operation is denied due to system state.
        Returns False if the agent is insolvent.
        Returns True if the operation is allowed.
        """
        # 1. Check Technical Axioms (Thermal Guard)
        hw_state = self.manager.hardware_state
        if hw_state:  # If HW state is available
            cpu_temp = getattr(hw_state, "cpu_temp", 0.0)
            gpu_temp = getattr(hw_state, "gpu_temp", 0.0)
            current_temp = max(cpu_temp, gpu_temp)

            if current_temp > self.config.thermal_limit_celsius:
                raise ResourceExhaustionHalt(
                    f"THERMAL GUARD TRIGGERED: System temp {current_temp}°C exceeds limit."
                )

            # Load Shedding
            current_load = (
                max(
                    getattr(hw_state, "cpu_load", 0.0),
                    getattr(hw_state, "gpu_load", 0.0),
                )
                / 100.0
            )
            if current_load > self.config.load_shedding_threshold:
                # If system is under heavy load, prioritize Live Game State
                if priority < PriorityLevel.LIVE_GAME_STATE:
                    # Staking Mechanism: Lower priority tasks are shed first
                    raise ResourceExhaustionHalt(
                        f"LOAD SHEDDING: Priority {priority.name} insufficient for current load {current_load * 100}%."
                    )

        # 2. Check Solvency (The Ledger)
        solvent = await self.manager.check_solvency(
            agent_id, required_cc=estimated_cost + self.config.min_solvency_buffer
        )
        if not solvent:
            # Strict enforcement: No credits, no compute.
            # "Halt Logic: If an agent's account reaches zero... issue RESOURCE_EXHAUSTION_HALT"
            raise ResourceExhaustionHalt(
                f"INSOLVENCY: Agent {agent_id} lacks sufficient Compute Credits."
            )

        return True

    def calculate_stake(self, priority: PriorityLevel) -> float:
        """
        Calculate the required 'stake' or surcharge for high-priority access.
        Live Game State might require a higher initial balance/stake to ensure completion.
        """
        if priority >= PriorityLevel.LIVE_GAME_STATE:
            return 50.0  # High stake requirement
        return 0.0

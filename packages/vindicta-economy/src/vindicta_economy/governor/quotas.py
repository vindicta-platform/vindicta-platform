from enum import Enum
from typing import Dict, Optional, Protocol


# Define Operation Types
class OperationType(str, Enum):
    BSH_GENERATION = "bsh_generation"
    DMF_EVALUATION = "dmf_evaluation"
    ALPHA_BETA_SEARCH = "alpha_beta_search"
    ORACLE_TRAINING_BATCH = "oracle_training_batch"


# Define Hardware State Protocol to decouple from vindicta-agents
class HardwareStateProtocol(Protocol):
    cpu_load: float
    gpu_load: float
    cpu_temp: float
    gpu_temp: float
    thermal_status: str  # "nominal", "warning", "critical"


class MockHardwareState:
    cpu_load: float = 0.0
    gpu_load: float = 0.0
    cpu_temp: float = 45.0
    gpu_temp: float = 40.0
    thermal_status: str = "nominal"


# Base Costs
COST_TABLE: Dict[OperationType, float] = {
    OperationType.BSH_GENERATION: 1.0,
    OperationType.DMF_EVALUATION: 5.0,
    OperationType.ALPHA_BETA_SEARCH: 2.0,  # Base base for exponential calc
    OperationType.ORACLE_TRAINING_BATCH: 500.0,
}


class ResourceQuotas:
    """
    Calculates the 'Cost of Truth' for engine operations.
    """

    @staticmethod
    def calculate_cost(
        op_type: OperationType,
        hardware_state: Optional[HardwareStateProtocol] = None,
        **kwargs,
    ) -> float:
        """
        Calculate the cost of an operation based on its type and current hardware state.

        Args:
            op_type: The type of operation.
            hardware_state: Current state of the hardware (optional).
            **kwargs: Additional parameters for specific operations (e.g., 'depth' for search).

        Returns:
            The calculated cost in Compute Credits (CC).
        """
        base_cost = COST_TABLE.get(op_type, 1.0)

        # apply operation-specific modifiers
        if op_type == OperationType.ALPHA_BETA_SEARCH:
            depth = kwargs.get("depth", 1)
            # Exponential cost: base * (2^depth) roughly, or simpler curve?
            # Prompt says "Exponential cost".
            # Let's use 2 as the base for the exponent.
            # Depth 1 = 2 * 2^0 = 2
            # Depth 2 = 2 * 2^1 = 4
            # Depth 3 = 2 * 2^2 = 8
            # Depth 4 = 2 * 2^3 = 16
            base_cost = base_cost * (2 ** (max(0, depth - 1)))

        # apply hardware state modifiers (Gas Metering / Thermal Throttling)
        multiplier = 1.0
        if hardware_state:
            if hardware_state.thermal_status == "critical":
                multiplier = 100.0  # Prohibitive cost
            elif hardware_state.thermal_status == "warning":
                multiplier = 2.0

            # Linear load scaling
            if hardware_state.cpu_load > 80.0:
                multiplier *= 1.5

        return base_cost * multiplier

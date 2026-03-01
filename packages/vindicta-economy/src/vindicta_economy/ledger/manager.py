import asyncio

from vindicta_economy.ledger.atomic_credits import (
    AtomicLedger,
    ComputeCreditTransaction,
)
from vindicta_economy.governor.quotas import (
    ResourceQuotas,
    OperationType,
    HardwareStateProtocol,
    MockHardwareState,
)


class VoidBankerManager:
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self, db_path: str = "compute_ledger.db"):
        self.ledger = AtomicLedger(db_path=db_path)
        self.quotas = ResourceQuotas()
        self.hardware_state: HardwareStateProtocol = MockHardwareState()

    @classmethod
    async def get_instance(cls, db_path: str = "compute_ledger.db"):
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls(db_path)
            return cls._instance

    def update_hardware_state(self, state: HardwareStateProtocol):
        """Update the internal hardware state for pricing calculations."""
        self.hardware_state = state

    async def check_solvency(self, agent_id: str, required_cc: float) -> bool:
        """
        Check if an agent has enough credits for the operation.
        This is a pre-check and does not deduct credits.
        """
        balance = await self.ledger.get_balance(agent_id)
        return balance >= required_cc

    async def purchase_operation(
        self, agent_id: str, op_type: OperationType, depth: int = 1
    ) -> bool:
        """
        Attempt to purchase an operation.
        Calculates cost, checks solvency, and deducts credits if sufficient.
        Returns True if successful, False otherwise.
        """
        cost = self.quotas.calculate_cost(
            op_type, hardware_state=self.hardware_state, depth=depth
        )

        # Transaction structure
        txn = ComputeCreditTransaction(
            id=f"txn_{agent_id}_{op_type.value}_{asyncio.get_event_loop().time()}",  # Simple ID generation
            agent_id=agent_id,
            action_type=op_type.value,
            amount=cost,
            metadata={"depth": depth}
            if op_type == OperationType.ALPHA_BETA_SEARCH
            else {},
        )

        success = await self.ledger.record_transaction(txn)
        return success

    async def grant_credits(self, agent_id: str, amount: float):
        """Admin function to grant credits."""
        await self.ledger.credit_account(agent_id, amount)

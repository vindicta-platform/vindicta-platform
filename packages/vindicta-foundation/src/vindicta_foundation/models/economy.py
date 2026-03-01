from pydantic import Field

from vindicta_foundation.models.base import VindictaModel


class GasTankState(VindictaModel):
    """Tracks the economic state of the platform to prevent runaway AI costs.

    Constitutional Compliance:
    - Rule II: Gas Tank Model must enforce hard limits on API spend.
    """

    balance_usd: float = Field(
        0.0, ge=0.0, description="Current available balance in USD"
    )
    limit_usd: float = Field(0.0, ge=0.0, description="Maximum allowed spend")
    is_active: bool = Field(
        True, description="Whether the tank is currently fueling operations"
    )

    @property
    def is_empty(self) -> bool:
        """Determines if the gas tank has no remaining funds.

        Returns:
            bool: True if the balance is less than or equal to 0.0, False otherwise.
        """
        return self.balance_usd <= 0.0

    @property
    def is_low(self) -> bool:
        """Determines if the gas tank is below 10% capacity relative to its limit.

        Returns:
            bool: True if the balance is less than 10% of the limit or if the \
                limit is 0 or less, False otherwise.
        """
        if self.limit_usd <= 0:
            return True
        return self.balance_usd < (self.limit_usd * 0.1)

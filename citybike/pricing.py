"""
Pricing strategies for trip cost calculation (Strategy Pattern).

"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------

class PricingStrategy(ABC):
    """Abstract pricing strategy — computes the cost of a trip."""

    @abstractmethod
    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Return the trip cost in euros.

        Args:
            duration_minutes: Length of the trip in minutes.
            distance_km: Distance traveled in kilometers.

        Returns:
            Trip cost as a float.
        """
        ...


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class CasualPricing(PricingStrategy):
    """Pricing for casual (non-member) users.

    Rate:
        - €1.00 unlock fee
        - €0.15 per minute
        - €0.10 per km
    """

    UNLOCK_FEE = 1.00
    PER_MINUTE = 0.15
    PER_KM = 0.10

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Compute trip cost for casual users."""
        return (
            self.UNLOCK_FEE
            + self.PER_MINUTE * duration_minutes
            + self.PER_KM * distance_km
        )


class MemberPricing(PricingStrategy):
    """Pricing for member users — discounted rates.

    Member rates:
        - No unlock fee
        - €0.08 per minute
        - €0.05 per km
    """

    UNLOCK_FEE = 0.0  # Members have no unlock fee
    PER_MINUTE = 0.08
    PER_KM = 0.05

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Compute trip cost for member users (no unlock fee)."""
        return self.UNLOCK_FEE + self.PER_MINUTE * duration_minutes + self.PER_KM * distance_km


class PeakHourPricing(PricingStrategy):
    """Pricing during peak hours (surcharge on top of casual rates).

    Applies a 1.5x multiplier to the CasualPricing cost.
    """

    MULTIPLIER = 1.5

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Compute trip cost during peak hours based on CasualPricing."""
        base_cost = CasualPricing().calculate_cost(duration_minutes, distance_km)
        return base_cost * self.MULTIPLIER


# ---------------------------------------------------------------------------
# Optional: Additional strategies
# ---------------------------------------------------------------------------

class FreeRidePromotion(PricingStrategy):
    """Promotional pricing: free rides under 10 minutes."""

    MAX_FREE_MINUTES = 10

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Return 0 for short trips, otherwise use CasualPricing."""
        if duration_minutes <= self.MAX_FREE_MINUTES:
            return 0.0
        return CasualPricing().calculate_cost(duration_minutes, distance_km)


# ---------------------------------------------------------------------------
# Example usage (for testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    duration = 25.0  # minutes
    distance = 5.0   # km

    casual_cost = CasualPricing().calculate_cost(duration, distance)
    print(f"Casual user cost: €{casual_cost:.2f}")

    member_cost = MemberPricing().calculate_cost(duration, distance)
    print(f"Member user cost: €{member_cost:.2f}")

    peak_cost = PeakHourPricing().calculate_cost(duration, distance)
    print(f"Peak hour cost: €{peak_cost:.2f}")

    free_cost = FreeRidePromotion().calculate_cost(8, 2)
    print(f"Free ride (8 min): €{free_cost:.2f}")

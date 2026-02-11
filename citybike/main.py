"""
CityBike — Bike-Sharing Analytics Platform
===========================================

Entry point that orchestrates the full pipeline:
    1. Load raw data
    2. Inspect & clean data
    3. Run analytics (business questions)
    4. Run numerical computations
    5. Generate visualizations
    6. Export summary report

Usage:
    python main.py
"""

from analyzer import BikeShareSystem
from visualization import (
    plot_trips_per_station,
    plot_monthly_trend,
    plot_duration_histogram,
    plot_duration_by_user_type,
)
from pricing import CasualPricing, MemberPricing, PeakHourPricing
from numerical import calculate_fares
import numpy as np


def main() -> None:
    """Run the complete CityBike analytics pipeline."""

    # ------------------------------
    # Initialize system
    # ------------------------------
    system = BikeShareSystem()

    # ------------------------------
    # Step 1 — Load data
    # ------------------------------
    print("\n>>> Loading data …")
    system.load_data()  # Loads trips.csv, stations.csv, maintenance.csv

    # ------------------------------
    # Step 2 — Inspect
    # ------------------------------
    print("\n>>> Inspecting data …")
    system.inspect_data()  # Prints basic info, missing values, first 3 rows

    # ------------------------------
    # Step 3 — Clean
    # ------------------------------
    print("\n>>> Cleaning data …")
    system.clean_data()  # Deduplicate, parse dates, numeric conversion, missing values, export cleaned CSVs

    # ------------------------------
    # Step 4 — Analytics
    # ------------------------------
    print("\n>>> Running analytics …")
    summary = system.total_trips_summary()
    print(f"  Total trips      : {summary['total_trips']}")
    print(f"  Total distance   : {summary['total_distance_km']} km")
    print(f"  Avg duration     : {summary['avg_duration_min']} min")

    # Additional analytics calls (example usage):
    # Top 10 start stations
    top_stations = system.top_start_stations()
    print("\nTop 10 Start Stations:")
    print(top_stations.to_string(index=False))

    # Peak usage hours
    peak_hours = system.peak_usage_hours()
    print("\nTrip counts by hour of day:")
    print(peak_hours)

    # Busiest day of week
    busiest_days = system.busiest_day_of_week()
    print("\nTrip counts by day of week:")
    print(busiest_days)

    # Average distance by user type
    avg_distance = system.avg_distance_by_user_type()
    print("\nAverage trip distance by user type:")
    print(avg_distance)

    # Monthly trip trend
    monthly_trend = system.monthly_trip_trend()
    print("\nMonthly trip trend:")
    print(monthly_trend)

    # Top active users
    top_users = system.top_active_users()
    print("\nTop active users:")
    print(top_users.to_string(index=False))

    # Maintenance cost by bike type
    maint_cost = system.maintenance_cost_by_bike_type()
    print("\nMaintenance cost by bike type:")
    print(maint_cost)

    # Top routes
    top_routes = system.top_routes()
    print("\nTop routes (start → end):")
    print(top_routes.to_string(index=False))

    # ------------------------------
    # Step 4b — Pricing (Strategy Pattern + NumPy vectorized fares)
    # ------------------------------
    print("\n>>> Calculating fares using pricing strategies …")
    casual_strategy = CasualPricing()
    member_strategy = MemberPricing()
    peak_strategy = PeakHourPricing()

    # Calculate fares for casual users
    casual_mask = system.trips["user_type"] == "casual"
    casual_trips = system.trips[casual_mask]
    casual_fares = calculate_fares(
        durations=casual_trips["duration_minutes"].to_numpy(),
        distances=casual_trips["distance_km"].to_numpy(),
        per_minute=casual_strategy.PER_MINUTE,
        per_km=casual_strategy.PER_KM,
        unlock_fee=casual_strategy.UNLOCK_FEE,
    )
    print(f"  Casual revenue   : €{np.sum(casual_fares):.2f}")

    # Calculate fares for member users
    member_mask = system.trips["user_type"] == "member"
    member_trips = system.trips[member_mask]
    member_fares = calculate_fares(
        durations=member_trips["duration_minutes"].to_numpy(),
        distances=member_trips["distance_km"].to_numpy(),
        per_minute=member_strategy.PER_MINUTE,
        per_km=member_strategy.PER_KM,
        unlock_fee=member_strategy.UNLOCK_FEE,
    )
    print(f"  Member revenue   : €{np.sum(member_fares):.2f}")

    # Optionally, calculate peak hour fares
    # peak_mask = (system.trips['start_time'].dt.hour >= 17) & (system.trips['start_time'].dt.hour <= 19)
    # peak_trips = system.trips[peak_mask]
    # peak_fares = calculate_fares(
    #     durations=peak_trips["duration_minutes"].to_numpy(),
    #     distances=peak_trips["distance_km"].to_numpy(),
    #     per_minute=casual_strategy.PER_MINUTE * peak_strategy.MULTIPLIER,
    #     per_km=casual_strategy.PER_KM * peak_strategy.MULTIPLIER,
    #     unlock_fee=casual_strategy.UNLOCK_FEE * peak_strategy.MULTIPLIER,
    # )

    # ------------------------------
    # Step 5 — Visualizations
    # ------------------------------
    print("\n>>> Generating visualizations …")
    plot_trips_per_station(system.trips, system.stations)
    plot_monthly_trend(system.trips)
    plot_duration_histogram(system.trips)
    plot_duration_by_user_type(system.trips)

    # ------------------------------
    # Step 6 — Report
    # ------------------------------
    print("\n>>> Generating summary report …")
    system.generate_summary_report()

    print("\n>>> Done! Check output/ for results.")


if __name__ == "__main__":
    main()

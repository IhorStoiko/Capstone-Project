"""
Data analysis engine for the CityBike platform.

Contains the BikeShareSystem class that orchestrates:
    - CSV loading and cleaning
    - Answering business questions using Pandas
    - Generating summary reports

Students should implement the cleaning logic and at least 10 analytics methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:
    """Central analysis class — loads, cleans, and analyzes bike-share data.

    Attributes:
        trips: DataFrame of trip records.
        stations: DataFrame of station metadata.
        maintenance: DataFrame of maintenance records.
    """

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection (provided)
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            print(f"\n{'='*40}")
            print(f"  {name}")
            print(f"{'='*40}")
            print(df.info())
            print(f"\nMissing values:\n{df.isnull().sum()}")
            print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """Clean all DataFrames and export to CSV.

        Steps implemented:
            1. Remove duplicate rows
            2. Parse date/datetime columns
            3. Convert numeric columns stored as strings
            4. Handle missing values
            5. Remove invalid entries
            6. Standardize categorical values
            7. Export cleaned data
        """
        if self.trips is None:
            raise RuntimeError("Call load_data() first")

        # --- Step 1: Remove duplicates ---
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        self.stations = self.stations.drop_duplicates(subset=["station_id"])
        self.maintenance = self.maintenance.drop_duplicates(subset=["record_id"])

        # --- Step 2: Parse dates ---
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"])
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"])
        self.stations["install_date"] = pd.to_datetime(self.stations["install_date"], errors='coerce')

        # --- Step 3: Convert numeric columns ---
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors='coerce')
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors='coerce')
        self.maintenance["cost_eur"] = pd.to_numeric(self.maintenance["cost_eur"], errors='coerce')

        # --- Step 4: Handle missing values ---
        self.trips["duration_minutes"].fillna(self.trips["duration_minutes"].median(), inplace=True)
        self.trips["distance_km"].fillna(self.trips["distance_km"].median(), inplace=True)
        self.trips["user_type"].fillna("casual", inplace=True)
        self.trips["status"].fillna("completed", inplace=True)

        # --- Step 5: Remove invalid entries ---
        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]]

        # --- Step 6: Standardize categorical values ---
        self.trips["status"] = self.trips["status"].str.lower().str.strip()
        self.trips["user_type"] = self.trips["user_type"].str.lower().str.strip()

        # --- Step 7: Export cleaned datasets ---
        DATA_DIR.mkdir(exist_ok=True)
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)

        print("Cleaning complete.")

    # ------------------------------------------------------------------
    # Analytics — Business Questions
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        counts = self.trips["start_station_id"].value_counts().head(n).reset_index()
        counts.columns = ["station_id", "trip_count"]
        return counts.merge(self.stations[["station_id", "name"]], on="station_id").sort_values(by="trip_count", ascending=False)

    def peak_usage_hours(self) -> pd.Series:
        return self.trips["start_time"].dt.hour.value_counts().sort_index()

    def busiest_day_of_week(self) -> pd.Series:
        return self.trips["start_time"].dt.day_name().value_counts().sort_values(ascending=False)

    def avg_distance_by_user_type(self) -> pd.Series:
        return self.trips.groupby("user_type")["distance_km"].mean()

    def monthly_trip_trend(self) -> pd.Series:
        return self.trips.groupby(self.trips["start_time"].dt.to_period("M")).size()

    def top_active_users(self, n: int = 15) -> pd.DataFrame:
        return self.trips.groupby("user_id").size().sort_values(ascending=False).head(n).reset_index(name="trip_count")

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        return self.maintenance.groupby("bike_type")["cost_eur"].sum()

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        counts = self.trips.groupby(["start_station_id", "end_station_id"]).size().reset_index(name="trip_count")
        return counts.sort_values(by="trip_count", ascending=False).head(n)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  CityBike — Summary Report")
        lines.append("=" * 60)

        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"  Total trips       : {summary['total_trips']}")
        lines.append(f"  Total distance    : {summary['total_distance_km']} km")
        lines.append(f"  Avg duration      : {summary['avg_duration_min']} min")

        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        print(f"Report saved to {report_path}")

"""
Matplotlib visualizations for the CityBike platform.

Students should create at least 4 charts:
    1. Bar chart — trips per station or revenue by user type
    2. Line chart — monthly trip trend over time
    3. Histogram — trip duration or distance distribution
    4. Box plot — duration by user type or bike type

All charts must have: title, axis labels, legend (where applicable).
Export each chart as PNG to output/figures/.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent / "output" / "figures"


def _save_figure(fig: plt.Figure, filename: str) -> None:
    """Save a Matplotlib figure to the figures directory."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filepath}")


# ---------------------------------------------------------------------------
# 1. Bar chart (provided as example)
# ---------------------------------------------------------------------------

def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    """Bar chart showing the number of trips starting at each station.

    Args:
        trips: Cleaned trips DataFrame.
        stations: Stations DataFrame (for station names).
    """
    # Count trips per start_station_id, take top 10
    counts = (
        trips["start_station_id"]
        .value_counts()
        .head(10)
        .rename_axis("station_id")
        .reset_index(name="trip_count")
    )
    # Merge with station names for labels
    merged = counts.merge(
        stations[["station_id", "station_name"]],
        on="station_id",
        how="left",
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(merged["station_name"], merged["trip_count"], color="steelblue")
    ax.set_xlabel("Number of Trips")
    ax.set_ylabel("Station")
    ax.set_title("Top 10 Start Stations by Trip Count")
    ax.invert_yaxis()  # highest count on top
    _save_figure(fig, "trips_per_station.png")


# ---------------------------------------------------------------------------
# 2. Line chart — monthly trend
# ---------------------------------------------------------------------------

def plot_monthly_trend(trips: pd.DataFrame) -> None:
    """Line chart of monthly trip counts.

    Extract year-month from start_time, group and count trips,
    then plot a line chart.
    """
    # Ensure start_time is datetime
    trips["start_time"] = pd.to_datetime(trips["start_time"])

    # Extract year-month as 'YYYY-MM'
    trips["year_month"] = trips["start_time"].dt.to_period("M").astype(str)

    # Count trips per month
    monthly_counts = trips.groupby("year_month").size()

    # Plot line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_counts.index, monthly_counts.values, marker="o", color="orange")
    ax.set_xlabel("Month (YYYY-MM)")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Monthly Trip Volume Trend")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle="--", alpha=0.5)
    _save_figure(fig, "monthly_trend.png")


# ---------------------------------------------------------------------------
# 3. Histogram — trip duration distribution
# ---------------------------------------------------------------------------

def plot_duration_histogram(trips: pd.DataFrame) -> None:
    """Histogram of trip durations.

    Plot the distribution of trips["duration_minutes"].
    """
    durations = trips["duration_minutes"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(durations, bins=30, color="skyblue", edgecolor="black")
    ax.set_xlabel("Trip Duration (minutes)")
    ax.set_ylabel("Number of Trips")
    ax.set_title("Distribution of Trip Durations")
    ax.grid(True, linestyle="--", alpha=0.5)
    _save_figure(fig, "duration_histogram.png")


# ---------------------------------------------------------------------------
# 4. Box plot — duration by user type
# ---------------------------------------------------------------------------

def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    """Box plot comparing trip durations across user types."""
    # Extract data per user_type
    data_to_plot = [group["duration_minutes"].values for _, group in trips.groupby("user_type")]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.boxplot(data_to_plot, labels=trips["user_type"].unique())
    ax.set_xlabel("User Type")
    ax.set_ylabel("Trip Duration (minutes)")
    ax.set_title("Trip Duration by User Type")
    ax.grid(True, linestyle="--", alpha=0.5)
    _save_figure(fig, "duration_by_user_type.png")

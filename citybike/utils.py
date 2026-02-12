"""
Utility helpers for the CityBike platform.

"""

import re
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

VALID_BIKE_TYPES = {"classic", "electric"}
VALID_USER_TYPES = {"casual", "member"}
VALID_TRIP_STATUSES = {"completed", "cancelled"}
VALID_MAINTENANCE_TYPES = {
    "tire_repair",
    "brake_adjustment",
    "battery_replacement",
    "chain_lubrication",
    "general_inspection",
}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_positive(value: float, name: str = "value") -> float:
    """Ensure *value* is a positive number.

    
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def validate_non_negative(value: float, name: str = "value") -> float:
    """Ensure *value* is zero or positive."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value


def validate_email(email: str) -> str:
    """Basic email validation — checks for presence of '@' and valid format."""
    if not isinstance(email, str) or "@" not in email:
        raise ValueError(f"Invalid email: {email!r}")
    # Optional stricter regex validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email!r}")
    return email


def validate_in(value: Any, allowed: set, name: str = "value") -> Any:
    """Ensure *value* is in the *allowed* set."""
    if value not in allowed:
        raise ValueError(f"{name} must be one of {allowed}, got {value!r}")
    return value


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_datetime(text: str) -> datetime:
    """Parse a datetime string in YYYY-MM-DD HH:MM:SS format."""
    try:
        return datetime.strptime(text, DATETIME_FORMAT)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {text!r}") from e


def parse_date(text: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(text, DATE_FORMAT)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {text!r}") from e


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_duration(minutes: float) -> str:
    """Format a duration in minutes as 'Xh Ym'.

    Example:
        >>> fmt_duration(95.5)
        '1h 35m'
    """
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h}h {m}m"


def fmt_currency(amount: float) -> str:
    """Format a monetary amount with two decimal places.

    Example:
        >>> fmt_currency(9.5)
        '€9.50'
    """
    return f"€{amount:.2f}"

# ==========================================
# STUDENT TEST TEMPLATE
# ==========================================
# Requires: pip install pytest
# ==========================================

from datetime import date
import pytest

# Assuming your updated functional code is in a file named health_stats_func.py
from health_stats_func import (
    create_daily_health_stats,
    add_steps,
    calculate_bmi,
    estimate_stride_m,
    calculate_km_walked,
    calculate_goal_progress_percent,
    is_goal_achieved,
)


# ==========================================
# Pytest Fixtures (Setup Data)
# ==========================================
@pytest.fixture
def default_stats():
    """Provides a standard baseline dictionary for basic feature testing."""
    return create_daily_health_stats(
        1.80,
        82.5,
        5000,
        1500,
        72
    )


# ==========================================
# Test Cases
# ==========================================


def test_initialization_with_defaults(default_stats):
    """Test that all metrics initialize correctly and date defaults to today."""
    assert default_stats["steps"] == 5000



def test_initialization_with_custom_date():
    """Test that a specific historic date can be explicitly recorded."""
    stats = create_daily_health_stats(
        1.80,
        82.5,
        5000,
        1500,
        72,
        log_date=date(2026, 10, 25)
    )

    assert stats["log_date"] == date(2026, 10, 25)


def test_bmi_calculation(default_stats):
    """Test standard BMI calculation: weight / height^2.

    For 82.5kg and 1.80m, BMI should equal 25.46.
    """
    assert calculate_bmi(default_stats) == 25.46


def test_bmi_raises_value_error_for_invalid_height():
    """Test that an invalid height of 0 or below throws a ValueError."""
    stats = create_daily_health_stats(
        0,
        82.5,
        5000,
        1500,
        72
    )

    with pytest.raises(ValueError):
        calculate_bmi(stats)


def test_estimated_stride_length(default_stats):
    """Test that stride length defaults strictly to 0.414 * height.

    For 1.80m, stride should round to 0.75m.
    """
    assert estimate_stride_m(default_stats) == 0.75 



def test_km_walked_calculation(default_stats):
    """Test distance calculation: (steps * stride) / 1000.

    5,000 steps * 0.75m stride = 3,750m -> 3.75 km.
    """
    assert calculate_km_walked(default_stats) == 3.75


def test_km_walked_with_zero_steps():
    """Test that distance is exactly 0.00 when zero steps are logged."""
    stats = create_daily_health_stats(
        1.80,
        82.5,
        0,
        1500,
        72
    )

    assert calculate_km_walked(stats) == 0


def test_initialization_with_custom_step_goal():
    """Test that a non-default step goal can be successfully initialized."""
    stats = create_daily_health_stats(
        1.80,
        82.5,
        5000,
        1500,
        72,
        step_goal=12000
    )

    assert stats["step_goal"] == 12000


def test_add_steps_increments_total(default_stats):
    """Test that calling add_steps increases the steps attribute properly."""
 
    add_steps(default_stats, 1000)

    assert default_stats["steps"] == 6000


def test_add_steps_raises_error_for_negative_values(default_stats):
    """Test that passing a negative step count throws a ValueError."""
    with pytest.raises(ValueError):
        add_steps(default_stats, -100)


def test_goal_progress_percentage(default_stats):
    """Test progress percentages under, at, and over the goal mark."""
    assert calculate_goal_progress_percent(default_stats) == 50



def test_goal_achieved_status(default_stats):
    """Test the boolean flag tracking if a goal milestone was crossed."""
    assert is_goal_achieved(default_stats) is False


def test_goal_progress_raises_error_for_invalid_goal():
    """Test that a goal configuration of zero or lower causes a ValueError."""
    stats = create_daily_health_stats(
        1.80,
        82.5,
        5000,
        1500,
        72,
        step_goal=0
    )

    with pytest.raises(ValueError):
        calculate_goal_progress_percent(stats)

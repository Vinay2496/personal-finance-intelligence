from app.services.forecasting import (
    _moving_average_forecast,
    _exponential_smoothing_forecast,
    _next_month_str,
    _evaluate_method,
)


def test_moving_average_basic():
    values = [100, 200, 300]
    result = _moving_average_forecast(values, window=3)
    assert result == 200


def test_moving_average_window_larger_than_data():
    values = [100, 200]
    result = _moving_average_forecast(values, window=3)
    assert result == 150


def test_exponential_smoothing_basic():
    values = [100, 200]
    result = _exponential_smoothing_forecast(values, alpha=0.5)
    # smoothed = 0.5*200 + 0.5*100 = 150
    assert result == 150


def test_next_month_str_normal():
    assert _next_month_str("2026-08") == "2026-09"


def test_next_month_str_year_rollover():
    assert _next_month_str("2026-12") == "2027-01"


def test_evaluate_method_too_few_points():
    values = [100, 200]
    result = _evaluate_method(values, _moving_average_forecast, window=3)
    assert result is None


def test_evaluate_method_returns_mae():
    values = [100, 100, 100, 100]
    result = _evaluate_method(values, _moving_average_forecast, window=3)
    # Perfectly flat data should have MAE of 0
    assert result == 0
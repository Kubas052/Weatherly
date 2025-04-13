''' Tests for weather_api.py, currently from chatGPT'''

from unittest.mock import patch
from datetime import datetime
import pytest
from core.utils.weather_api import WeatherAPI


@pytest.fixture
def api():
    return WeatherAPI()

@patch("core.utils.weather_api.requests.get")
def test_get_current_weather(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"weather": "sunny"}

    result = api.get_weather("current", "London")
    assert result == {"weather": "sunny"}
    assert mock_get.called
    assert "weather" in mock_get.call_args[0][0]


@patch("core.utils.weather_api.requests.get")
def test_get_daily_forecast(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"forecast": "rain"}

    result = api.get_weather("daily_forecast", "Paris")
    assert result["forecast"] == "rain"


@patch("core.utils.weather_api.requests.get")
def test_get_hourly_forecast(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"hourly": True}

    result = api.get_weather("hourly_forecast", "Berlin")
    assert result["hourly"] is True


@patch("core.utils.weather_api.requests.get")
def test_get_historical_weather(mock_get, api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"history": "data"}

    test_date = datetime(2024, 1, 1)
    result = api.get_weather("historical", "Tokyo", date=test_date, days=2)
    assert "history" in result


@patch("core.utils.weather_api.requests.get")
def test_invalid_request_type_raises(api, mock_get):
    with pytest.raises(ValueError):
        api.get_weather("invalid_type", "Madrid")

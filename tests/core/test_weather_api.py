import pytest
import requests
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from core.utils.weather_api import WeatherAPI


class TestWeatherAPI:
    """Test suite for WeatherAPI class."""

    @patch.object(WeatherAPI, '_make_request')
    def test_get_weather_current(self, mock_make_request):
        """Test get_weather with current weather request."""
        mock_make_request.return_value = {'current': 'weather'}
        
        weather_api = WeatherAPI()
        result = weather_api.get_weather("current", "Warsaw")
        
        assert result == {'current': 'weather'}
        mock_make_request.assert_called_once_with(
            f"{weather_api.base_url}weather",
            {'q': 'Warsaw', 'units': 'metric'}
        )

    @patch.object(WeatherAPI, '_make_request')
    def test_get_weather_daily(self, mock_make_request):
        """Test get_weather with daily forecast request."""
        mock_make_request.return_value = {'daily': 'forecast'}
        
        weather_api = WeatherAPI()
        result = weather_api.get_weather("daily", "London")
        
        assert result == {'daily': 'forecast'}
        mock_make_request.assert_called_once_with(
            f"{weather_api.base_url}forecast/daily",
            {'q': 'London', 'units': 'metric', 'cnt': 16}
        )

    @patch.object(WeatherAPI, '_make_request')
    def test_get_weather_hourly(self, mock_make_request):
        """Test get_weather with hourly forecast request."""
        mock_make_request.return_value = {'hourly': 'forecast'}
        
        weather_api = WeatherAPI()
        result = weather_api.get_weather("hourly", "Paris")
        
        assert result == {'hourly': 'forecast'}
        mock_make_request.assert_called_once_with(
            f"{weather_api.base_url}forecast/hourly",
            {'q': 'Paris', 'units': 'metric'}
        )

    @patch.object(WeatherAPI, '_make_request')
    def test_get_weather_historical(self, mock_make_request):
        """Test get_weather with historical data request."""
        mock_make_request.return_value = {'history': 'data'}
        test_date = datetime(2023, 1, 1)
        
        weather_api = WeatherAPI()
        result = weather_api.get_weather("historical", "Berlin", date=test_date, days=3)
        
        assert result == {'history': 'data'}
        expected_params = {
            'q': 'Berlin',
            'units': 'metric',
            'date': test_date,
            'days': 3,
            'start': int(test_date.timestamp()),
            'end': int(test_date.timestamp()) + 3 * 86400
        }
        mock_make_request.assert_called_once_with(
            f"{weather_api.history_url}city",
            expected_params
        )

    def test_get_weather_invalid_type(self):
        """Test get_weather with invalid request type."""
        weather_api = WeatherAPI()
        with pytest.raises(ValueError, match="Nieprawidłowy typ żądania"):
            weather_api.get_weather("invalid_type", "Madrid")

"""Module for interacting with OpenWeatherMap API."""

from datetime import datetime
import requests
from .config import Config

# pylint: disable=too-few-public-methods
class WeatherAPI:
    """Provides a unified interface to request weather data."""

    def __init__(self):
        """Initializes the WeatherAPI with endpoint URLs and API key."""

        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.history_url = "https://history.openweathermap.org/data/2.5/history/"
        self.api_key = Config.API_KEY
    def _make_request(self, endpoint, params=None):
        """
        Internal method to send a GET request to a given endpoint.

        Args:
            endpoint (str): Full API URL.
            params (dict, optional): Query parameters.

        Returns:
            dict: JSON response from the API.
        """

        if params is None:
            params = {}
        params["appid"] = self.api_key
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        print("wykonuje sie _make_request()")
        print(response.url)
        print(response.status_code)
        return response.json()

    def get_weather(self, request_type, city, **kwargs):
        """
        Retrieves weather data based on request type.

        Args:
            request_type (str): One of
            'current', 'daily_forecast', 'hourly_forecast', or 'historical'.
            city (str): City name.
            kwargs: Additional parameters like 'date' and 'days' for historical data.

        Returns:
            dict: Weather data from the API.
        """
        params = {"q": city, "units": "metric"}

        if request_type == "current":
            endpoint = f"{self.base_url}weather"
        elif request_type == "daily":
            params.update({"cnt": 16})
            endpoint = f"{self.base_url}forecast/daily"
        elif request_type == "hourly":
            endpoint = f"{self.base_url}forecast/hourly"
        elif request_type == "historical":
            date = kwargs.get('date', datetime.now())
            days = min(kwargs.get('days', 1), 7) #Jestem dumny z tego zapisu
            start = int(date.timestamp())
            end = start + days * 86400
            params.update({"start": start, "end": end})
            endpoint = f"{self.history_url}city"

        else:
            raise ValueError("Nieprawidłowy typ żądania")

        params.update(kwargs)
        print(f"parametry to: {params}")
        return self._make_request(endpoint, params)

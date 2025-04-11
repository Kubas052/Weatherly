import requests
from datetime import datetime
from .config import Config


class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.history_url = "https://history.openweathermap.org/data/2.5/history/"
        self.api_key = Config.API_KEY
    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params["appid"] = self.api_key
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        print("TUTAJ")
        print(response.url)
        return response.json()

    def get_weather(self, request_type, city, **kwargs):
        params = {"q": city, "units": "metric"}

        if request_type == "current":
            endpoint = f"{self.base_url}weather"
        elif request_type == "daily_forecast":
            endpoint = f"{self.base_url}forecast/daily"
        elif request_type == "hourly_forecast":
            endpoint = f"{self.base_url}forecast/hourly"
        elif request_type == "historical":
            date = kwargs.get('date', datetime.now())
            days = min(kwargs.get('days', 1), 7) #Jestem dumny z tego zapisu
            start = int(date.timestamp()-864000)
            end = start + days * 86400
            params.update({"start": start, "end": end})
            endpoint = f"{self.history_url}city"
        else:
            raise ValueError("Nieprawidłowy typ żądania")

        params.update(kwargs)
        return self._make_request(endpoint, params)
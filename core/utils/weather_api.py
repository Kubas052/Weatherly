import requests
from .config import Config
from datetime import datetime


class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.history_url = "https://history.openweathermap.org/data/2.5/history/"
        self.api_key = Config.API_KEY

    def do_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params["appid"] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()  # checks HTTP errors
        return response.json()

    def get_current_weather(self, city: str):
        return self.do_request("weather", {"q": city})

    def get_forecast_daily(self, city: str):
        return self.do_request("forecast/daily", {"q": city})

    def get_forecast_hourly(self, city: str):
        return self.do_request("forecast/hourly", {"q": city})

    def get_history(self, city: str, date: datetime, days: int = 1):
        start = int(date.timestamp())
        end = start + days * 86400
        if days > 7:
            print("Max 7 days, reducing to 7 days")
            days = 7
            end = start + 7 * 86400

        params = {
            "q": city,
            "start": start,
            "end": end,
            "units": "metric",
            "appid": self.api_key
        }

        response = requests.get(f"{self.history_url}city", params=params)
        response.raise_for_status()
        return response.json()
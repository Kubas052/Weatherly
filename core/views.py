from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .utils.weather_api import WeatherAPI
def index(request):
    return render(request, 'core/index.html')

def weather_view(request):
    city = request.GET.get('city', 'Warsaw')
    weather_api = WeatherAPI()

    try:
        current_weather  = weather_api.get_current_weather(city)
        weather_text = f"""
        Current weather in {city}:
        Temperature: {current_weather['main']['temp']}
        Conditions: {current_weather['weather'][0]['description']}
        Humidity: {current_weather['main']['humidity']}%
        """
        return HttpResponse(weather_text, content_type="text/plain")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", content_type="text/plain")
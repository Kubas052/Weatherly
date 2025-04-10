from django.shortcuts import render


# Create your views here.
from .utils.weather_api import WeatherAPI
def index(request):
    return render(request, 'core/index.html')


def weather_view(request):
    context = {'success': False}

    try:
        city = request.GET.get('city', 'Warsaw')
        api = WeatherAPI()
        weather_data = api.get_weather('current', city)
        context = {
            'city': city,
            'temperature': round(weather_data['main']['temp'], 1),
            'description': weather_data['weather'][0]['description'].capitalize(),
            'icon': weather_data['weather'][0]['icon'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'success': True
        }
    except Exception as e:
        context['error'] = f"Błąd: {str(e)}"
    return render(request, 'core/weather_view.html', context)
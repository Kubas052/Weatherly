from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse

# Create your views here.
from .utils.weather_api import WeatherAPI
def index(request):
    return render(request, 'core/index.html')


def weather_view(request):
    context = {'success': False}

    try:
        city = request.GET.get('city')  or 'Warsaw'
        historical_start_date = request.GET.get('historical_start_date') or 'None'
        historical_length = request.GET.get('historical_length') or 'None'
        view_type = request.GET.get('view_type') or 'current'
        print(view_type)
        print(historical_length)
        print(historical_start_date)
        api = WeatherAPI()
        weather_data = api.get_weather(view_type, city)
        if view_type == 'current':
            context = {
                'city': city,
                'temperature': round(weather_data['main']['temp'], 1),
                'description': weather_data['weather'][0]['description'].capitalize(),
                'icon': weather_data['weather'][0]['icon'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed'],
                'success': True
            }
            return render(request, 'core/weather_view.html', context)
        elif view_type == 'historical':
            historical_list = []
            for i, hour_data in enumerate(weather_data['list']):
                dt = hour_data['dt']
                hour = datetime.fromtimestamp(dt).strftime('%H:%M')
                if i > 0:
                    prev_dt = weather_data['list'][i - 1]['dt']
                    delta_hours = int((dt - prev_dt) / 3600)
                    historical_list.append({
                        'hour': hour,
                        'temp': round(hour_data['main']['temp'], 1),
                        'feels_like': round(hour_data['main']['feels_like'], 1),
                        'humidity': hour_data['main']['humidity'],
                        'wind_speed': hour_data['wind']['speed'],
                        'description': hour_data['weather'][0]['description'].capitalize(),
                        'delta_hours': delta_hours
                    })
                else:
                    print(None)
                    delta_hours = None

            context = {
                'city': city,
                'forecast_data': historical_list,
                'success': True
            }
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(context)
            return render(request, 'core/historical_view.html', context)

    except Exception as e:
        context['error'] = f"Błąd: {str(e)}"

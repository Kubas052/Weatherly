from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.core.exceptions import ValidationError

# Create your views here.
from .utils.weather_api import WeatherAPI
def index(request):
    return render(request, 'core/index.html')


def weather_view(request):
    context = {'success': False}

    try:
        city = request.GET.get('city')  or 'Warsaw'
        historical_start_date = request.GET.get('historical_start_date') or 'None'
        historical_length = int(request.GET.get('historical_length')) or 'None'
        view_type = request.GET.get('view_type') or 'current'

        api = WeatherAPI()

        if view_type == 'current':
            print("WYKONALA SIE SEKCJA CURRENT")
            weather_data = api.get_weather(view_type, city)
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
            print("WYKONALA SIE SEKCJA HISTORICAL")
            if not historical_start_date:
                raise ValidationError("Historical start date is required")
            date_obj = datetime.strptime(historical_start_date, '%Y-%m-%d')
            print(f"Przekazywana data do WeatherAPI: {date_obj.isoformat()}")
            weather_data = api.get_weather(
                view_type,
                city,
                date=date_obj,
                days=historical_length
            )
            historical_list = []
            for i, hour_data in enumerate(weather_data['list']):
                dt = hour_data['dt']
                date_time = datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
                hour = datetime.fromtimestamp(dt).strftime('%H:%M')
                if i > 0:
                    prev_dt = weather_data['list'][i - 1]['dt']
                    delta_hours = int((dt - prev_dt) / 3600)
                    historical_list.append({
                        'datetime': date_time,
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
        elif view_type == 'daily':
            print("WYKONALA SIE SEKCJA DAILY")
            weather_data = api.get_weather(view_type, city)
            forecast_list = []

            for i, day_data in enumerate(weather_data['list']):
                dt = day_data['dt']
                date = datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
                day_name = datetime.fromtimestamp(dt).strftime('%A')  # Nazwa dnia tygodnia

                # Dla każdego dnia dodajemy tylko jeden wpis (pomijamy godzinę)
                forecast_list.append({
                    'date': date,
                    'day_name': day_name,
                    'day_temp': round(day_data['temp']['day']),
                    'min_temp': round(day_data['temp']['min']),
                    'max_temp': round(day_data['temp']['max']),
                    'night_temp': round(day_data['temp']['night']),
                    'eve_temp': round(day_data['temp']['eve']),
                    'morn_temp': round(day_data['temp']['morn']),
                    'humidity': day_data['humidity'],
                    'pressure': day_data['pressure'],
                    'description': day_data['weather'][0]['description'].capitalize(),
                    'icon': day_data['weather'][0]['icon'],
                    'wind_speed': day_data['speed'],
                    'rain': day_data.get('rain', 0)  # Użyj get() bo nie zawsze jest 'rain'
                })

            context = {
                'city': city,
                'city_data': weather_data['city'],  # Używamy pełnych danych miasta z API
                'forecast_data': forecast_list,
                'success': True
            }
            print(forecast_list)
            return render(request, 'core/forecast_daily_view.html', context)
        elif view_type == 'hourly':
            print("WYKONALA SIE SEKCJA HOURLY")
            weather_data = api.get_weather(view_type, city)
            forecast_list = []
            for i, hour_data in enumerate(weather_data['list']):
                dt = hour_data['dt']
                date_time = datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M')
                hour = datetime.fromtimestamp(dt).strftime('%H:%M')
                if i > 0:
                    prev_dt = weather_data['list'][i - 1]['dt']
                    delta_hours = int((dt - prev_dt) / 3600)
                    forecast_list.append({
                        'datetime': date_time,
                        'hour': hour,
                        'temp': round(hour_data['main']['temp'], 1),
                        'feels_like': round(hour_data['main']['feels_like'], 1),
                        'humidity': hour_data['main']['humidity'],
                        'wind_speed': hour_data['wind']['speed'],
                        'description': hour_data['weather'][0]['description'].capitalize(),
                        'delta_hours': delta_hours
                    })
                context = {
                    'city': city,
                    'city_data': weather_data['city'],  # Używamy pełnych danych miasta z API
                    'forecast_data': forecast_list,
                    'success': True
                }
            return render(request, 'core/forecast_hourly_view.html', context)
    except Exception as e:
        context['error'] = f"Błąd: {str(e)}"
    return render(request, 'core/index.html', context)
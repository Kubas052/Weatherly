from dotenv import load_dotenv
import os
load_dotenv()
class Config:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    DEFAULT_CITY = "Warsaw"
    units_options = {
        '1': {'name': 'Celsius (°C)', 'value': 'metric'},
        '2': {'name': 'Fahrenheit (°F)', 'value': 'imperial'},
        '3': {'name': 'Kelvin (K)', 'value': 'standard'}
    }
    default_city = 'Warsaw'
    UNITS = units_options['1']['value']

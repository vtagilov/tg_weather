import json
import requests
from dataclasses import dataclass

WEATHER_API = (
    "https://api.open-meteo.com/v1/"
    "forecast?&current_weather=true"
    "&timezone=Europe%2FMoscow"
    "&latitude={latitude}"
    "&longitude={longitude}"
)

ROUND_WIND_SPEED = 1
SEC_IN_HOUR = 3600
METRES_PER_KILOMETER = 1000

file_weather_codes = open('weather_codes.json', "r", encoding='utf-8')
weather_codes = json.load(file_weather_codes)
file_weather_codes.close()


@dataclass(slots=True, frozen=True)
class Weather:
    latitude: float
    longitude: float
    address: str
    temperature: float
    wind_speed: float
    weather_description: str


def get_weather_api(latitude: float, longitude: float, address: str) -> Weather:
    weather_data = requests.get(WEATHER_API.format(latitude=latitude, longitude=longitude)).json()
    return Weather(
        latitude=latitude,
        longitude=longitude,
        temperature=weather_data["current_weather"]["temperature"],
        wind_speed=round(weather_data["current_weather"]["windspeed"] *
                         METRES_PER_KILOMETER / SEC_IN_HOUR, ROUND_WIND_SPEED),
        weather_description=weather_codes[str(weather_data["current_weather"]["weathercode"])],
        address=address
    )


def get_weather_info(latitude: float, longitude: float, address="") -> str:
    weather = get_weather_api(latitude=latitude, longitude=longitude, address=address)
    if address != "":

        return (
                "В " + weather.address + " " + weather.weather_description + "\n" +
                str(weather.temperature) + "°C\n" +
                str(weather.wind_speed) + " м/с"
        )
    else:
        return (
                "За окном " + weather.weather_description + "\n" +
                str(weather.temperature) + "°C\n" +
                str(weather.wind_speed) + " м/с"
        )

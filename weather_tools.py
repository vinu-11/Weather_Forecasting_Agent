import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")


def get_current_weather(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    data = requests.get(url).json()

    if str(data.get("cod")) == "404":
        raise ValueError("City not found")

    if "main" not in data:
        raise ValueError(
            data.get("message", "Unable to fetch weather data")
        )

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }


def get_forecast(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    data = requests.get(url).json()

    if str(data.get("cod")) == "404":
        raise ValueError("City not found")

    forecast = []

    for item in data["list"]:

        forecast.append({
            "datetime": item["dt_txt"],
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "rain": item.get("pop", 0) * 100
        })

    return forecast


def get_coordinates(city):

    url = (
        f"http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={API_KEY}"
    )

    data = requests.get(url).json()

    if not data:
        raise ValueError("City not found")

    return data[0]["lat"], data[0]["lon"]


def get_air_quality(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    data = requests.get(url).json()

    return data["list"][0]
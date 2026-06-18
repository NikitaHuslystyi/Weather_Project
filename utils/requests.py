import requests
from config import API_KEY


def request(city_name, request_type, lang="uk"):
    if request_type == "current_weather":
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang={lang}")
    elif request_type == "daily_forecast":
        response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric&lang={lang}")
    data = response.json()
    return data
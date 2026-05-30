import requests
from config import API_KEY


def request(city_name, request_type):
    if request_type == "current_weather":
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ua")
    elif request_type == "daily_forecast":
        response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric&lang=ua")
    data = response.json()
    return data
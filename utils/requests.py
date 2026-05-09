import requests
from config import API_KEY


def request(city_name):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric&lang=ua")
    data = response.json()
    city = data["name"]
    temp = round(data["main"]["temp"])
    max_temp = round(data["main"]["temp_max"])
    max_temp = round(data["main"]["temp_max"])
    min_temp = round(data["main"]["temp_min"])
    return data
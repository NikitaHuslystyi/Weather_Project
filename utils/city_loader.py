import json
import os
import threading
import requests


def get_cities_list(base_dir):
    path = os.path.join(base_dir, "json", "cities.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data and isinstance(data[0], str):
            return load_cities(base_dir)
        return data
    except Exception:
        return []


def load_cities(base_dir):
    response = requests.get("https://countriesnow.space/api/v0.1/countries")
    data = response.json()
    result = []
    for country in data["data"]:
        for city in country["cities"]:
            result.append({"city": city, "country": country["country"]})
    result = sorted(result, key=lambda x: x["city"])
    path = os.path.join(base_dir, "json", "cities.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    return result


def ensure_cities_loaded(base_dir):
    path = os.path.join(base_dir, "json", "cities.json")
    needs_reload = False
    if not os.path.exists(path):
        needs_reload = True
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data and isinstance(data[0], str):
                needs_reload = True
        except Exception:
            needs_reload = True
    if needs_reload:
        thread = threading.Thread(target=load_cities, args=(base_dir,), daemon=True)
        thread.start()
import json
import os
import requests
from config import API_KEY


def load_translations(base_dir):
    path = os.path.join(base_dir, "json", "translate.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        translations = {}
        for item in data:
            eng_name = item.get("name", "")
            if eng_name:
                translations[eng_name] = {
                    "uk": item.get("uk", eng_name),
                    "en": item.get("en", eng_name),
                }
        return translations
    except Exception:
        return {}


def get_city_display_name(city_translations, english_name, lang_code="ua"):
    entry = city_translations.get(english_name)
    if not entry:
        return english_name
    if lang_code == "ua":
        return entry.get("uk") or english_name
    return entry.get("en") or english_name


def fetch_city_translation(base_dir, city_translations, city_name, translation_in_progress):
    if city_name in city_translations:
        return
    if city_name in translation_in_progress:
        return
    translation_in_progress.add(city_name)

    path = os.path.join(base_dir, "json", "translate.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    except Exception:
        existing = []

    if any(item.get("name") == city_name for item in existing):
        translation_in_progress.discard(city_name)
        return

    try:
        response = requests.get(
            f"https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
        )
        data = response.json()
        if data:
            local_names = data[0].get("local_names", {})
            uk_name = local_names.get("uk", city_name)
            en_name = local_names.get("en", city_name)
            existing.append({"name": city_name, "uk": uk_name, "en": en_name})
            with open(path, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=4)
            city_translations[city_name] = {"uk": uk_name, "en": en_name}
    except Exception as e:
        print(f"Помилка перекладу {city_name}: {e}")
    finally:
        translation_in_progress.discard(city_name)
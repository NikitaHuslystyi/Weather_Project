import os
import json


def json_write(file_name, data):
    path = os.path.abspath(os.path.join(__file__, "..", "..", "json", file_name))
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
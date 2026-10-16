"""
Завдання 2:
Провалідуйте, чи усі файли у папці ideas_for_test/work_with_json є валідними json.
результат для невалідного файлу виведіть через логер на рівні еррор у файл json__kamalov.log.
"""
import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "json__kamalov.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("json_validator")

for filename in sorted(os.listdir(BASE_DIR)):
    if not filename.endswith(".json"):
        continue

    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"{filename}: VALID")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file '{filename}': {e}")
        print(f"{filename}: INVALID")

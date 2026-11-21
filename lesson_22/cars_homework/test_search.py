import logging
import os

import pytest
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8080"
USERNAME = "test_user"
PASSWORD = "test_pass"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_search.log")

# Логування і в консоль, і в файл test_search.log
logger = logging.getLogger("test_search")
logger.setLevel(logging.INFO)
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    for handler in (logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")):
        handler.setFormatter(formatter)
        logger.addHandler(handler)

# Дані по машинах (ті самі, що в cars_db сервера)
CARS = [
    {"brand": "BMW", "year": 2018, "engine_volume": 2.0, "price": 50000},
    {"brand": "Audi", "year": 2020, "engine_volume": 1.8, "price": 45000},
    {"brand": "Mercedes", "year": 2019, "engine_volume": 2.5, "price": 55000},
    {"brand": "Toyota", "year": 2017, "engine_volume": 2.4, "price": 35000},
    {"brand": "Honda", "year": 2016, "engine_volume": 1.6, "price": 30000},
    {"brand": "Nissan", "year": 2021, "engine_volume": 1.5, "price": 40000},
    {"brand": "Ford", "year": 2015, "engine_volume": 2.2, "price": 32000},
    {"brand": "Chevrolet", "year": 2018, "engine_volume": 1.8, "price": 28000},
    {"brand": "Volkswagen", "year": 2019, "engine_volume": 2.0, "price": 33000},
    {"brand": "Hyundai", "year": 2020, "engine_volume": 1.6, "price": 29000},
    {"brand": "Kia", "year": 2019, "engine_volume": 2.0, "price": 31000},
    {"brand": "Subaru", "year": 2017, "engine_volume": 2.5, "price": 40000},
    {"brand": "Mazda", "year": 2018, "engine_volume": 2.0, "price": 32000},
    {"brand": "Lexus", "year": 2021, "engine_volume": 3.0, "price": 60000},
    {"brand": "Infiniti", "year": 2019, "engine_volume": 3.5, "price": 52000},
    {"brand": "Acura", "year": 2020, "engine_volume": 2.4, "price": 48000},
    {"brand": "Jeep", "year": 2018, "engine_volume": 3.6, "price": 45000},
    {"brand": "Land Rover", "year": 2020, "engine_volume": 2.0, "price": 55000},
    {"brand": "Volvo", "year": 2019, "engine_volume": 2.0, "price": 46000},
    {"brand": "Porsche", "year": 2021, "engine_volume": 3.0, "price": 70000},
    {"brand": "Tesla", "year": 2020, "engine_volume": 0.0, "price": 80000},
    {"brand": "Ferrari", "year": 2021, "engine_volume": 6.3, "price": 250000},
    {"brand": "Lamborghini", "year": 2020, "engine_volume": 6.5, "price": 300000},
    {"brand": "Bugatti", "year": 2019, "engine_volume": 8.0, "price": 350000},
    {"brand": "McLaren", "year": 2021, "engine_volume": 4.0, "price": 280000},
]


def expected_cars(sort_by, limit):
    """Очікуваний результат: сортування (за замовчуванням за brand) + обрізка по limit."""
    key = sort_by if sort_by else "brand"
    result = sorted(CARS, key=lambda car: car[key])
    return result[:limit] if limit else result


@pytest.fixture(scope="class")
def auth_session():
    """Первинна аутентифікація: один раз на клас, токен прописується в заголовки сесії."""
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    assert response.status_code == 200, response.text
    session.headers.update({"Authorization": "Bearer " + response.json()["access_token"]})
    logger.info("Аутентифікація пройшла, токен додано в заголовки сесії")
    yield session
    session.close()


class TestSearchCars:
    @pytest.mark.parametrize(
        "sort_by, limit",
        [
            ("price", 5),
            ("year", 3),
            ("engine_volume", 10),
            ("brand", 7),
            (None, 4),        # без sort_by -> сортування за brand
            ("price", None),  # без limit -> усі 25 машин
            ("year", 25),     # limit дорівнює кількості машин у базі
        ],
    )
    def test_search_cars(self, auth_session, sort_by, limit):
        params = {}
        if sort_by is not None:
            params["sort_by"] = sort_by
        if limit is not None:
            params["limit"] = limit

        response = auth_session.get(f"{BASE_URL}/cars", params=params)
        logger.info("GET /cars params=%s -> %s", params, response.status_code)

        assert response.status_code == 200
        assert response.json() == expected_cars(sort_by, limit)

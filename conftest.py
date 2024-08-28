import pytest
import requests
import random
import string
from varaibles import *


@pytest.fixture(scope="function")
def generate_random_string():
    def _generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    return _generate_random_string


@pytest.fixture(scope="function")
def new_courier(generate_random_string):
    courier_data = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }
    yield courier_data

    # Удаление курьера после завершения теста
    response = requests.post(f"{BASE_URL_FIXTURE}/courier/login", json={
        "login": courier_data['login'],
        "password": courier_data['password']
    })
    if response.status_code == 200:
        courier_id = response.json()['id']
        requests.delete(f"{BASE_URL_FIXTURE}/courier/{courier_id}")


@pytest.fixture(scope="function")
def created_courier(new_courier):
    response = requests.post(f"{BASE_URL_FIXTURE}/courier", json=new_courier)
    assert response.status_code == 201, "Failed to create a new courier"
    return new_courier


@pytest.fixture(scope="function")
def order_data(generate_random_string):
    data = {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": generate_random_string(),
        "metroStation": str(random.randint(1, 10)),
        "phone": "+7" + ''.join(random.choices(string.digits, k=10)),
        "rentTime": random.randint(1, 10),
        "deliveryDate": "2024-08-20",
        "comment": generate_random_string(),
        "color": random.choice([["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    }
    return data


@pytest.fixture(scope="function")
def create_order(order_data):
    response = requests.post(f"{BASE_URL_FIXTURE}/orders", json=order_data)
    assert response.status_code == 201, "Failed to create an order"
    return response.json()

import pytest
import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

@allure.epic("Получение списка заказов")
class TestGetOrders:

    def test_get_orders_list(self):
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

import pytest
import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

@allure.epic("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test Street, 1",
            "metroStation": 1,
            "phone": "+79000000000",
            "rentTime": 5,
            "deliveryDate": "2024-08-20",
            "comment": "Test order",
            "color": color
        }

        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()

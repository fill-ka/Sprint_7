import pytest
import requests
import allure
from varaibles import *


@allure.epic("Создание заказа")
class TestCreateOrder:

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_various_colors(self, order_data, color):
        order_data["color"] = color
        response = requests.post(BASE_URL_ORDERS, json=order_data)
        assert response.status_code == 201, "Failed to create order"
        assert "track" in response.json()

    def test_create_order_without_color(self, order_data):
        del order_data["color"]
        response = requests.post(BASE_URL_ORDERS, json=order_data)
        assert response.status_code == 201, "Failed to create order"
        assert "track" in response.json()

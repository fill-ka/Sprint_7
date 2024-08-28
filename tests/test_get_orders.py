import pytest
import requests
import allure
from varaibles import *


@allure.epic("Получение списка заказов")
class TestGetOrders:

    def test_get_orders_list(self):
        response = requests.get(BASE_URL_ORDERS)
        assert response.status_code == 200, "Failed to get orders list"
        assert isinstance(response.json(), dict)
        assert "orders" in response.json()

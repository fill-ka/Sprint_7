import pytest
import requests
import allure
from varaibles import *


@allure.epic("Создание курьера")
class TestCreateCourier:

    def test_create_courier_success(self, new_courier):
        response = requests.post(BASE_URL_COURIER, json=new_courier)
        assert response.status_code == 201, "Failed to create courier"
        assert response.json()["ok"] == True

    def test_create_duplicate_courier(self, created_courier):
        response = requests.post(BASE_URL_COURIER, json=created_courier)
        assert response.status_code == 409, "Expected 409 when creating a duplicate courier"

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field, new_courier):
        courier_data = new_courier.copy()
        del courier_data[missing_field]
        response = requests.post(BASE_URL_COURIER, json=courier_data)
        assert response.status_code == 400, f"Expected 400 when missing {missing_field}"

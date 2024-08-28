import pytest
import requests
import allure
from varaibles import *

@allure.epic("Логин курьера")
class TestCourierLogin:
    def test_courier_login_success(self, created_courier):
        response = requests.post(BASE_URL_COURIER, json={
            "login": created_courier["login"],
            "password": created_courier["password"]})

        assert response.status_code == 200, "Failed to login courier"
        assert "id" in response.json()

    def test_courier_login_invalid_credentials(self, created_courier):
        response = requests.post(BASE_URL_COURIER, json={
            "login": created_courier["login"],
            "password": "wrongpassword"
        })
        assert response.status_code == 404, "Expected 404 when logging in with invalid credentials"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_login_missing_field(self, missing_field, created_courier):
        login_data = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        del login_data[missing_field]
        response = requests.post(BASE_URL_COURIER, json=login_data)
        assert response.status_code == 400, f"Expected 400 when missing {missing_field}"

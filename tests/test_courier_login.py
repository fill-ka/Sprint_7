import pytest
import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

@allure.epic("Логин курьера")
class TestCourierLogin:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.login = self.generate_random_string()
        self.password = self.generate_random_string()
        self.first_name = self.generate_random_string()

        requests.post(BASE_URL, json={"login": self.login, "password": self.password, "firstName": self.first_name})

        yield

        self.delete_courier(self.login, self.password)

    def generate_random_string(self, length=10):
        import random, string
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def delete_courier(self, login, password):
        response = requests.post(f"{BASE_URL}/login", json={"login": login, "password": password})
        if response.status_code == 200:
            courier_id = response.json().get("id")
            requests.delete(f"{BASE_URL}/{courier_id}")

    def test_courier_login_success(self):
        response = requests.post(f"{BASE_URL}/login", json={"login": self.login, "password": self.password})

        assert response.status_code == 200
        assert "id" in response.json()

    def test_courier_login_invalid_credentials(self):
        response = requests.post(f"{BASE_URL}/login", json={"login": self.login, "password": "wrong_password"})

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_login_missing_field(self, missing_field):
        payload = {"login": self.login, "password": self.password}
        del payload[missing_field]

        response = requests.post(f"{BASE_URL}/login", json=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text

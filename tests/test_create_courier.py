import pytest
import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

@allure.epic("Создание курьера")
class TestCreateCourier:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.login = self.generate_random_string()
        self.password = self.generate_random_string()
        self.first_name = self.generate_random_string()

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

    def test_create_courier_success(self):
        payload = {"login": self.login, "password": self.password, "firstName": self.first_name}
        response = requests.post(BASE_URL, json=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_duplicate_courier(self):
        payload = {"login": self.login, "password": self.password, "firstName": self.first_name}
        requests.post(BASE_URL, json=payload)

        response = requests.post(BASE_URL, json=payload)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {"login": self.login, "password": self.password, "firstName": self.first_name}
        del payload[missing_field]

        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text

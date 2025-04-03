import allure
import jsonschema
import requests
from .schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        response = requests.get(f'{BASE_URL}/store/order/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Размещение заказа питомца")
    def test_create_order(self):
        with allure.step("Подготовка данных для создания заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId заказа не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity заказа не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f'{BASE_URL}/store/order/{order_id}')

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_id, "id заказа не совпадает с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            orderId = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(f'{BASE_URL}/store/order/{orderId}')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f'{BASE_URL}/store/order/{orderId}')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(f'{BASE_URL}/store/inventory')

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert isinstance(response.json()["approved"], int), "Ожидалось числовое значение approved"
            assert isinstance(response.json()["delivered"], int), "Ожидалось числовое значение delivered"
import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.random_string import generate_random_string


@allure.feature("Create user tests")
class TestUserRegister(BaseCase):
    exclude_params = [
        ("email"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("password")
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        # print(response.status_code)
        # print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_wrong_email(self):
        email = "testexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        # print("\n")
        # print(response.status_code)
        # print(response.content)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == 'Invalid email format'

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("exclude", exclude_params)
    def test_create_user_without_one_field(self, exclude):
        data = self.prepare_registration_data()
        data.pop(exclude)

        response = MyRequests.post(url="/user/", data=data)
        # print("\n")
        # print(response.status_code)
        # print(response.content)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {exclude}", \
            f"Unexpected content{response.content}"

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        random_string = generate_random_string(1)
        data["username"] = random_string
        response = MyRequests.post(url="/user/", data=data)
        # print("\n")
        # print(response.status_code)
        # print(response.content)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short",\
            f"Unexpected content{response.content}"

    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_too_long_username(self):
        data = self.prepare_registration_data()
        random_string = generate_random_string(251)
        data["username"] = random_string
        response = MyRequests.post(url="/user/", data=data)
        # print("\n")
        # print(response.status_code)
        # print(response.content)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long",\
            f"Unexpected content{response.content}"
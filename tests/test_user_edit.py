from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
from lib.random_string import generate_random_string

class TestUserEdit(BaseCase):
    exclude_params = [
        ("incorrect_email"),
        ("too_short_first_name")
    ]

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = self.create_new_user(register_data)

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_not_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = self.create_new_user(register_data)

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed Name"
        response = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        # print("\n")
        # print(response.status_code)
        # print(response.content)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

    def test_edit_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = self.create_new_user(register_data)

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        new_user_id = int(user_id) - 1
        response = MyRequests.put(
            f"/user/{new_user_id}",
            data={"firstName": new_name}
        )
        # print("\n")
        # print(response.status_code)
        # print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("condition", exclude_params)
    def test_edit_user_email_and_first_name_with_incorrect_value(self, condition):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = self.create_new_user(register_data)

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        if condition == "incorrect_email":
            new_email = "newemailexample.com"

            response = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
            )
            # print("\n")
            # print(response.status_code)
            # print(response.content)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "Invalid email format", \
                f"Unexpected response content {response.content}"

        elif condition == "too_short_first_name":
            new_firstname = generate_random_string(1)

            response = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_firstname}
            )
            # print("\n")
            # print(response.status_code)
            # print(response.content)

            Assertions.assert_code_status(response, 400)
            assert response.json()["error"] == "Too short value for field firstName", \
                f"Unexpected response content {response.content}"



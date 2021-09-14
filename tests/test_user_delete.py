from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_try_delete_user_by_id(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # LOGIN
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # print("\n")
        # print(user_id_from_auth_method)

        data2 = {"user_id": user_id_from_auth_method}
        header = {"x-csrf-token": token}
        cookie = {"auth_sid": auth_sid}
        response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}", data=data2, headers=header, cookies=cookie)
        # print("\n")
        # print(response2.status_code)
        # print(response2.content)

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response content {response2.content}"

    def test_delete_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = self.create_new_user(register_data)

        email = register_data["email"]
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

        # DELETE
        data2 = {"user_id": user_id}
        header = {"x-csrf-token": token}
        cookie = {"auth_sid": auth_sid}
        response3 = MyRequests.delete(f"/user/{user_id}", data=data2, headers=header, cookies=cookie)

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # print("\n")
        # print(response4.status_code)
        # print(response4.content)

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response2.content}"

    def test_delete_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = self.create_new_user(register_data)

        email = register_data["email"]
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

        # DELETE
        user_id_other_user = int(user_id) - 1
        data2 = {"user_id": user_id}
        header = {"x-csrf-token": token}
        cookie = {"auth_sid": auth_sid}
        response3 = MyRequests.delete(f"/user/{user_id_other_user}", data=data2, headers=header, cookies=cookie)
        # There should be an error message that deletion is possible only for the current user

        Assertions.assert_code_status(response3, 200)

        # VERIFY
        response4 = MyRequests.get(f"/user/{user_id_other_user}", headers=header, cookies=cookie)
        # There should be a success message, the user was not deleted, 200 status-code is returned

        # print("\n")
        # print(response4.status_code)
        # print(response4.content)
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", \
            f"Unexpected response content {response4.content}"


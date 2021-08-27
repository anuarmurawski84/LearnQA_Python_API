import requests

def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    for i in dict(response.cookies):
        print(i)

    cookie_value = response.cookies.get('HomeWork')
    print(cookie_value)
    assert cookie_value == "hw_value", "Incorrect value"


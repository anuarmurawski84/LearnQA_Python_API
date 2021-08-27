import requests

def test_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    for i in dict(response.headers):
        print(i)

    header_value = response.headers.get("x-secret-homework-header")
    print(header_value)
    assert header_value == "Some secret value", "Incorrect value"
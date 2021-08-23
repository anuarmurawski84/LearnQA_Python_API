import requests

methods = {'POST', 'GET', 'PUT', 'DELETE', 'DELETE'}

link = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1
response = requests.post(link)
print(response.text)
print(response.status_code)
print("______________")

# 2
response_head = requests.head(link)
print(response_head.text)
print(response_head.status_code)
print("______________")

# 3
response_post = requests.post(link, data={"method": "POST"})
print(response_post.text)
print(response_post.status_code)
print("______________")

# 4

for method in methods:
    for method_ in methods:
        payload = {'method': method_}
        if method == 'GET':
            response = requests.request(method, link, params=payload)
        else:
            response = requests.request(method, link, data=payload)
        if method != method_ and response.status_code == 200 and response.text == '{"success":"!"}':
            print(f'method - {method} but method in parameters - {method_}, {response.text}, {response.status_code}')

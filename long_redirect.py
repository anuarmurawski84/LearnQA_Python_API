import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

sum = 0
for redirect in response.history[1:]:
    print(redirect.url)
    sum += 1

# Number of requests
print(sum)
# Last url
print(response.url)
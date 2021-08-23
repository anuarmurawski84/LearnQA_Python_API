import requests
import time

link = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1
response = requests.get(link)
token = response.json()['token']
seconds = response.json()['seconds']
#2-4
response = requests.get(link, params={'token': token})
print(response.status_code)
print(response.text)
status = response.json()['status']
if status == 'Job is NOT ready':
    time.sleep(seconds)
    response = requests.get(link, params={'token': token})
    status = response.json()['status']
    result = response.json()['result']
    if status == 'Job is ready' and result:
        print('Everything is fine')

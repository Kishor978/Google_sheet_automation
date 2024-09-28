import requests

url = 'http://127.0.0.1:5000/submit'
data = {
    "name": "Kishor Thagunna",
    "address": "Kanchanpur, Nepal",
    "contact": "9842997090",
    "email": "thaunnakishor@gmail.com"}

response = requests.post(url, json=data)
print(response.json())

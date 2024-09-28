import requests

url = 'http://127.0.0.1:5000/submit'
data = {
    "name": "Doe",
    "address": "123 Main St",
    "contact": "1234567890",
    "email": "john@example.com"
}

response = requests.post(url, json=data)
print(response.json())

import requests
from django.conf import settings  # To access Django settings

def create_order(data):
    url = "https://pre-alpha.ithinklogistics.com/api_v3/order/add.json"
    headers = {
        "Content-Type": "application/json",
        "Access-Token": settings.ITL_ACCESS_TOKEN,  # Replace with your actual access token
        "Secret-Key": settings.ITL_SECRET_KEY,  # Replace with your actual secret key
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors gracefully
        return {"error": "Failed to create the order", "status_code": response.status_code}
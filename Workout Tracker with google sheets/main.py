import os
import requests
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
TOKEN = os.environ.get("TOKEN")
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
    "Authorization": TOKEN
}
bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}


today = datetime.now()
today_formatted = today.strftime("%d/%m/%Y")
time_formatted = today.strftime("%X")




user_input = input("Tell me which excercises you did: ")

look_up_params = {
    "query": user_input
}
get_response = requests.post(
    url="https://trackapi.nutritionix.com/v2/natural/exercise",
    json=look_up_params,
    headers=headers,
)
get_data = get_response.json()

for exercise in get_data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_formatted,
            "time": time_formatted,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }


write_response = requests.post(
    url=SHEET_ENDPOINT,
    json=sheet_inputs,
    headers=bearer_headers,
)

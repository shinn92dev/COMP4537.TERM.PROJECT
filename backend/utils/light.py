import os
# import asyncio
import requests
from dotenv import load_dotenv
# from govee_api_laggat import Govee


load_dotenv()
URL = "https://developer-api.govee.com/v1/devices"

key = os.getenv("GOVEE_API_KEY")


def get_govee_devices(api_key):
    headers = {
        "Govee-API-Key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        devices = response.json().get("data", {}).get("devices", [])
        if not devices:
            print("❌ No devices found.")
            return
        return devices
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return


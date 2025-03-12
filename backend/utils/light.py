import os
# import asyncio
import requests
from dotenv import load_dotenv
# from govee_api_laggat import Govee


load_dotenv()
URL = "https://developer-api.govee.com/v1/devices"

key = os.getenv("GOVEE_API_KEY")


class Govee():
    def __init__(self, api_key):
        self.key = api_key
        self.devices = self.get_govee_devices(self.key)
        if self.devices:
            self.devices_num = len(self.devices)
        else:
            self.devices_num = 0

    def get_govee_devices(self, api_key):
        headers = {
            "Govee-API-Key": api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(URL, headers=headers)
        if response.status_code == 200:
            devices = response.json().get("data", {}).get("devices", [])
            if not devices:
                # TODO: Raise error later
                print("❌ No devices found.")
                return
            return devices
        else:
            # TODO: Raise error later
            print(f"❌ Error: {response.status_code} - {response.text}")
            return


g = Govee(key)

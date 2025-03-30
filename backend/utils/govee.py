import os
import uuid
import requests
import time
from dotenv import load_dotenv


load_dotenv()

key = os.getenv("GOVEE_API_KEY")


class Govee():
    def __init__(self, api_key):
        self.key = api_key
        self.base_url = "https://developer-api.govee.com/v1/devices/"
        self.headers = {
            "Govee-API-Key": api_key,
            "Content-Type": "application/json"
        }
        self.devices = self.get_govee_devices()
        if self.devices:
            self.devices_num = len(self.devices)
        else:
            self.devices_num = 0

    def get_govee_devices(self):
        response = requests.get(self.base_url, headers=self.headers)
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

    def _is_connected(self):
        return self.devices_num

    def turn_on_and_off(self, device: dict, on=True):
        url = self.base_url + "control"
        payload = {
            "requestId": str(uuid.uuid4()),
            "sku": device["model"],
            "device": device["device"],
            "model": device["model"],
            "cmd": {
                "type": "devices.capabilities.on_off",
                "instance": "powerSwitch",
                "name": "turn",
                "value": "on" if on else "off"
            },
        }
        response = requests.put(url, headers=self.headers, json=payload)
        time.sleep(1)
        if response.status_code == 200:
            state_emoji = "🌞" if on else "🌑"
            state = "on" if on else "off"
            print(f"{state_emoji} Light successfully turned {state}.")
            print(response.json())
        else:
            state = "on" if on else "off"
            print(f"❌Error during turning {state}: ", end="")
            try:
                result = response.json()
                print(result["message"])
            except Exception as e:
                print(e)

    def set_lamp_color(self, device, color):
        url = self.base_url + "control"
        payload = {
            "requestId": str(uuid.uuid4()),
            "sku": device["model"],
            "device": device["device"],
            "model": device["model"],
            "cmd": {
            "name": "color",
            "value": {
                "r": color["r"],
                "g": color["g"],
                "b": color["b"]
            }
        }
        }
        response = requests.put(url, headers=self.headers, json=payload)
        time.sleep(1)
        if response.status_code == 200:
            print(response.json())
        else:
            state = "on" if on else "off"
            print(f"❌Error during setting {state}: ", end="")
            try:
                result = response.json()
                print(result["message"])
            except Exception as e:
                print(e)


    def set_lamp_brightness(self, device: dict, brightness: int):
        url = self.base_url + "control"
        payload = {
        "requestId": str(uuid.uuid4()),
            "sku": device["model"],
            "device": device["device"],
            "model": device["model"],
            "cmd": {
                "name": "brightness",
                "value": brightness
            }
        }

        response = requests.put(url, headers=self.headers, json=payload)
        time.sleep(1)

        if response.status_code == 200:
            print(f"💡 Brightness set to {brightness} successfully.")
            print(response.json())
        else:
            print("❌ Error setting brightness: ", end="")
            try:
                print(response.json()["message"])
            except Exception as e:
                print(e)



def main():
    g = Govee(key)
    print(g.get_govee_devices())

    # for i in (range(5)):
    #     condition = True if i % 2 == 0 else False
    #     g.turn_on_and_off(1, condition)
    #     time.sleep(2)


if __name__ == "__main__":
    main()

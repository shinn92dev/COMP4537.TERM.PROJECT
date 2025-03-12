import os
import requests
from dotenv import load_dotenv


class Utils:
    def __init__(self) -> None:
        load_dotenv()
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather?"

    def get_weather(self, lat: float, lon: float) -> dict:
        key = os.getenv("OPEN_WEATHER_API_KEY")
        url = self.weather_url + f"lat={lat}&lon={lon}&appid={key}"
        response = requests.get(url)
        data = response.json()
        print(data)
        return data


test_locations = [
    [49.2827, -123.1207],  # 밴쿠버, 캐나다
    [37.5665, 126.9780],   # 서울, 대한민국
    [37.7749, -122.4194],  # 샌프란시스코, 미국
    [51.5074, -0.1278],    # 런던, 영국
    [35.6895, 139.6917],   # 도쿄, 일본
    [40.7128, -74.0060],   # 뉴욕, 미국
    [-33.8688, 151.2093],  # 시드니, 호주
    [48.8566, 2.3522],     # 파리, 프랑스
    [55.7558, 37.6173],    # 모스크바, 러시아
    [39.9042, 116.4074],   # 베이징, 중국
    [-23.5505, -46.6333]   # 상파울루, 브라질
]

u = Utils()
u.get_weather(test_locations[0][0], test_locations[0][1])

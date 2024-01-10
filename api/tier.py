import requests

class Tier:
    def __init__(self):
        self.url = "https://platform.tier-services.io/v2/vehicle?type%5B%5D=escooter&type%5B%5D=ebicycle"
        self.headers = {
            "User-Agent": "TIER/4.0.127 (Android/12)",
            "Customer-Agent": "Tier Android",
            "X-Api-Key": "iPtAHWdOVLEtgkaymXoMHVVg",
            "Host": "platform.tier-services.io",
        }

    def get_scooters(self, lat, lng, radius):
        response = requests.get(self.url + "&lat=" + str(lat) + "&lng=" + str(lng) + "&radius=" + str(radius), headers=self.headers)
        return response.json()
import requests
from vehicle import *

default_radius = 1370

class Tier:
    def __init__(self):
        self.url = "https://platform.tier-services.io/v2/vehicle?type%5B%5D=escooter&type%5B%5D=ebicycle"
        self.headers = {
            "User-Agent": "TIER/4.0.127 (Android/12)",
            "Customer-Agent": "Tier Android",
            "X-Api-Key": "iPtAHWdOVLEtgkaymXoMHVVg",
            "Host": "platform.tier-services.io",
        }

    def get_scooters(self, lat, lon, radius):
        response = requests.get(self.url + "&lat=" + str(lat) + "&lng=" + str(lon) + "&radius=" + str(radius), headers=self.headers)
        return response.json()
    
    def get_vehicles(self, init_lat, init_lon):
        json_obj = self.get_scooters(init_lat, init_lon, default_radius)
        all_vehicles = []
        data = json_obj.get("data", {})
        for row in data:
            if row.get("type", "") == "vehicle":
                vehicle_data = row.get("attributes", {})
                lat = row.get("lat", 0)
                lon = row.get("lon", 0)
                charge = row.get("batteryLevel", 0)
                range = row.get("currentRangeMeters", 0)

                vehicle = Vehicle(vehicle_type='scooter', charge=charge, lat=lat, lon=lon, brand='bolt', range=range)
                all_vehicles.append(vehicle)

        return all_vehicles

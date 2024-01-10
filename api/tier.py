import requests
from vehicle import *

default_location = (54.372158, 18.638306)
default_radius = 1370

class Tier:
    def __init__(self):
        self.url = "https://platform.tier-services.io/v2/vehicle?type%5B%5D=escooter&type%5B%5D=ebicycle"
        self.zones_url = "https://platform.tier-services.io/v1/zone/geo-rules?"
        self.headers = {
            "User-Agent": "TIER/4.0.127 (Android/12)",
            "Customer-Agent": "Tier Android",
            "X-Api-Key": "iPtAHWdOVLEtgkaymXoMHVVg",
            "Host": "platform.tier-services.io",
        }

    def get_scooters(self, lat = default_location[0], lon = default_location[1], radius = default_radius):
        response = requests.get(self.url + "&lat=" + str(lat) + "&lng=" + str(lon) + "&radius=" + str(radius), headers=self.headers)
        return response.json()
    
    def get_vehicles(self, init_lat = default_location[0], init_lon = default_location[1]):
        json_obj = self.get_scooters(init_lat, init_lon, default_radius)
        all_vehicles = []
        data = json_obj.get("data", {})
        for row in data:
            if row.get("type", "") == "vehicle":
                vehicle_data = row.get("attributes", {})
                if vehicle_data.get("isRentable", True):
                    lat = vehicle_data.get("lat", 0)
                    lon = vehicle_data.get("lng", 0)
                    charge = vehicle_data.get("batteryLevel", 0)
                    range = vehicle_data.get("currentRangeMeters", 0)

                    vehicle = Vehicle(vehicle_type='scooter', charge=charge, lat=lat, lon=lon, brand='tier', range=range)
                    all_vehicles.append(vehicle)

        return all_vehicles


    def get_zones(self, lat, lon):
        response = requests.get(self.url + "lat=" + str(lat) + "&lng=" + str(lon) + "&radius=100000", headers=self.headers)
        return response.json()
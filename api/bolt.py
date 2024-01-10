import requests
import json
from vehicle import *

default_location = (54.372158, 18.638306)

class Bolt:
    def __init__(self):
        self.url = "https://user.live.boltsvc.net/micromobility/search/getVehicles/v2?language=en&version=CA.97.1&deviceId=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7&device_name=XiaomiM2101K9AG&device_os_version=12&channel=googleplay&deviceType=android&"

        self.headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Host": "user.live.boltsvc.net",
            "Authorization": "Basic KzQ4NjY3ODIyODI0OjVkMGQ0YTZmLTkxNTktNGFiNC05NDAyLWMzMzkwY2NmNmI2NA=="
        }

    def get_scooters(self, lat = default_location[0], lon = default_location[1]):
        response = requests.post(self.url + "gps_lat=" + str(lat) + "&gps_lng=" + str(lon), headers=self.headers)
        return response.json()
    
    def get_vehicles(self, init_lat = default_location[0], init_lon = default_location[1]):
        json_obj = self.get_scooters(init_lat, init_lon)
        all_vehicles = []
        categories = json_obj.get("data", {}).get("categories", [])
        for category in categories:
            markers_on_map = category.get("markers_on_map", [])
            for marker in markers_on_map:
                vehicle_data = marker.get("vehicle", {})
                charge = vehicle_data.get("charge", 0)
                location = vehicle_data.get("location", {})
                lat = location.get("lat", None)
                lon = location.get("lng", None)
                if lat is not None and lon is not None:
                    vehicle = Vehicle(vehicle_type='scooter', charge=charge, lat=lat, lon=lon, brand='bolt')
                    all_vehicles.append(vehicle)
        return all_vehicles
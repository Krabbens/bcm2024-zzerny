import requests
import json

class Bolt:
    def __init__(self):
        self.url = "https://user.live.boltsvc.net/micromobility/search/getVehicles/v2?language=en&version=CA.97.1&deviceId=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7&device_name=XiaomiM2101K9AG&device_os_version=12&channel=googleplay&deviceType=android&gps_lat=54.354711&gps_lng=18.591989"

        self.headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Host": "user.live.boltsvc.net",
            "Authorization": "Basic KzQ4NjY3ODIyODI0OjVkMGQ0YTZmLTkxNTktNGFiNC05NDAyLWMzMzkwY2NmNmI2NA=="
        }

    def get_scooters(self, lat, lng):
        response = requests.post(self.url + "gps_lat=" + str(lat) + "&gps_lng=" + str(lng), headers=self.headers)
        return response.json()
    
    def get_locations(self):
        json_obj = self.get_scooters()
        all_vehicles = []
        categories = json_obj.get("data", {}).get("categories", [])
        for category in categories:
            markers_on_map = category.get("markers_on_map", [])
            for marker in markers_on_map:
                vehicle = marker.get("vehicle", {})
                all_vehicles.append(vehicle)

        # Wyświetlanie wyników
        for vehicle in all_vehicles:
            print(vehicle)

import requests
import json
from vehicle import *
from zone import *

default_location = (54.372158, 18.638306)

class Bolt:
    def __init__(self):
        self.scooters_url = "https://user.live.boltsvc.net/micromobility/search/getVehicles/v2?language=en&version=CA.97.1&deviceId=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7&device_name=XiaomiM2101K9AG&device_os_version=12&channel=googleplay&deviceType=android&"

        self.scooters_headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Host": "user.live.boltsvc.net",
            "Authorization": "Basic KzQ4NjY3ODIyODI0OjVkMGQ0YTZmLTkxNTktNGFiNC05NDAyLWMzMzkwY2NmNmI2NA=="
        }

        self.zones_url = "https://user.live.boltsvc.net/rental/cityArea/listByTile?tile_id=206%2C573&last_known_tile_version=20%3A1704811992%3A6947306752002353ff6404b76b936d72%3Ace29ad8fe1c0c01db44f4c46d304cdb8&version=CA.97.1&deviceId=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7&device_name=XiaomiM2101K9AG&device_os_version=12&channel=googleplay&deviceType=android&signup_session_id=2ef261b41127306e297dc19780e32506f019f97d68d21bcc5b682bd330687be6&country=pl&language=en&gps_lat=54.354711&gps_lng=18.591989&gps_accuracy_m=56.988&gps_age=46&user_id=92153560&session_id=92153560u1704892259654&distinct_id=client-92153560&rh_session_id=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7u1704892224"

        self.zones_headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Host": "user.live.boltsvc.net",
            "Authorization": "Basic KzQ4NjY3ODIyODI0OjVkMGQ0YTZmLTkxNTktNGFiNC05NDAyLWMzMzkwY2NmNmI2NA=="
        }
    
    def get_zones_json(self):
        response = requests.get(self.zones_url, headers=self.zones_headers)
        return response.json()
    
    def get_zones(self):
        json_obj = self.get_zones_json()
        all_zones = []
        data = json_obj["data"]
        area_groups = data["area_groups_by_ids"]
        areas = data["areas"]["added"]
        for a in areas:
            type = area_groups[a["group_id"]]["style_id"]
            zone = Zone(type=type,lat=0,lon=0,brand='bolt', geometry=None)
            all_zones.append(zone)
        return all_zones

    def get_scooters(self, lat = default_location[0], lon = default_location[1]):
        response = requests.post(self.scooters_url + "gps_lat=" + str(lat) + "&gps_lng=" + str(lon), headers=self.scooters_headers)
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
import requests
import json
from vehicle import *
from zone import *
from api.polyline import decode
import math

default_location = (54.372158, 18.638306)

big_square = [(54.293922117308036, 18.815218467247558),
              (54.46983576845764, 18.907679148240515),
              (54.65859820998237, 18.310232871255128),
              (54.03600955355388, 18.21188579748574)]

type_mapping = {
    'preferred_parking': 'parking',
    'mandatory_parking': 'parking-mode',
    'no_parking': 'no-parking',
    'speed_limited': 'reduced-speed',
    'no_parking_mandatory': 'no-parking',
    'mandatory_parking_vehicle_count_limited': 'parking-mode',
    'allowed': 'allowed',
    'no_parking_speed_limited': 'no-parking',
    'no_go_zone': 'no-go',
    'allowed_inverted': 'allowed'
}

def polacz_listy(tab1, tab2, element1, element2):
    wynik = []
    indeks1 = 0
    indeks2 = 0


    while indeks1 < len(tab1) and tab1[indeks1] != element1:
        wynik.append(tab1[indeks1])
        indeks1 += 1
    wynik.append(tab1[indeks1])
    while indeks2 < len(tab2) and tab2[indeks2] != element2:
        #wynik.append(tab2[indeks2])
        indeks2 += 1

    wynik.append(tab2[indeks2])
    indeks2 += 1
    if indeks2 >= len(tab2):
            indeks2 = 0

    while tab2[indeks2] != element2:
        wynik.append(tab2[indeks2])
        indeks2 += 1
        if indeks2 >= len(tab2):
            indeks2 = 0
    wynik.append(tab2[indeks2])
    while indeks1 < len(tab1):
        wynik.append(tab1[indeks1])
        indeks1 += 1
    wynik.append(tab1[0])    

    return wynik

def nearest_points(polygon1, polygon2):
    min = 9999999999
    min1 = 0
    min2 = 0
    for p1 in polygon1:
        for p2 in polygon2:
            dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            if dist < min:
                min = dist
                min1 = p1
                min2 = p2
    return min1, min2


def combine_polygons(polygon1, polygon2):
    point1, point2 = nearest_points(polygon1, polygon2)
    return polacz_listy(polygon1, polygon2, point1, point2)

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
    
    def get_inverted(self):
        json_obj = self.get_zones_json()
        all_geometries = []
        data = json_obj["data"]
        area_groups = data["inverted_area_groups_by_ids"]
        areas = data["inverted_areas"]["added"]
        for a in areas:
            all_geometries.append(decode(a["polygon"]["locations"]))
        
        if(len(all_geometries) > 0):
            combined = combine_polygons(all_geometries[0], all_geometries[1])
            i = 2
            while i < len(all_geometries):
                combined = combine_polygons(combined, all_geometries[i])
                i+=1
        else:
            combined = all_geometries[0]
        
        inverted = combine_polygons(combined, big_square)
        return Zone(type='allowed_inverted',lat=0,lon=0,brand='bolt', geometry=inverted)
        
        
    
    def get_zones(self):
        json_obj = self.get_zones_json()
        all_zones = []
        data = json_obj["data"]
        area_groups = data["area_groups_by_ids"]
        areas = data["areas"]["added"]
        for a in areas:
            type = type_mapping[area_groups[a["group_id"]]["style_id"]]
            zone = Zone(type=type,lat=0,lon=0,brand='bolt', geometry=decode(a["polygon"]["locations"]))
            all_zones.append(zone)
        all_zones.append(self.get_inverted())
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
import requests
from vehicle import *
from zone import *


default_location = (54.372158, 18.638306)
default_radius = 7000

class Tier:
    def __init__(self):
        self.url = "https://platform.tier-services.io/v2/vehicle?type%5B%5D=escooter&type%5B%5D=ebicycle"
        self.zones_url = "https://platform.tier-services.io/v1/zone/geo-rules?"
        self.geo_url = "https://platform.tier-services.io/v2/zone/root/"
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


    def get_zones_json(self, lat = default_location[0], lon = default_location[1]):
        response = requests.get(self.zones_url + "lat=" + str(lat) + "&lng=" + str(lon) + "&radius=100000", headers=self.headers)
        return response.json()
    
    def get_vec(self, root_zone):
        uri = self.geo_url + root_zone + "/geometry"
        response = requests.get(uri, headers=self.headers)
        data = response.json()
        new_geo = []
        for geo in data["data"]["features"]:
            poly = []
            for point in geo["geometry"]["coordinates"][0]:
                poly.append({"lat": point[1], "lng": point[0]})
            new_geo.append({"type": geo["properties"], "coordinates": poly})

    def get_geometry(self, root_zone):
        uri = self.geo_url + root_zone + "/geometry"
        response = requests.get(uri, headers=self.headers)
        return response.json()
    
    def get_zones(self, lat = default_location[0], lon = default_location[1]):
        json_obj = self.get_zones_json(lat, lon)
        all_geometry = []

        #getting unique rootZoneIds
        root_zones = list(set([i["attributes"]["rootZoneId"] for i in json_obj["data"]]))
        for ro in root_zones:
            geometry_json = self.get_geometry(ro)
            all_geometry.extend(geometry_json["data"]["features"])
        all_zones = []
        data = json_obj["data"]
        for zone in data:
            geo_id = zone["attributes"]["geometryId"]
            geometry = None
            for geo in all_geometry:
                if geo["id"] == geo_id:
                    geometry = [(y, x) for x, y in geo["geometry"]["coordinates"][0]]
                    break
            type = zone["attributes"]["spec"]
            if geometry != None:
                all_zones.append(Zone(geometry, type, 0, 0, brand="tier"))
        return all_zones


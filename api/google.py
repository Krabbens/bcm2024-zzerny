from api.bolt import * 
from api.tier import *
import requests

api_key = "AIzaSyAMKb9DtOMN4KlBkUKqg8zf0m_ks-Zcwp8"

class Google:
    def __init__(self):
        self.url = "https://user.live.boltsvc.net/micromobility/search/getVehicles/v2?language=en&version=CA.97.1&deviceId=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7&device_name=XiaomiM2101K9AG&device_os_version=12&channel=googleplay&deviceType=android&"


    def get_distances(self, waypoints_pairs):
        waypoints = [point for pair in waypoints_pairs for point in pair]

        base_url = "https://maps.googleapis.com/maps/api/directions/json"

        if len(waypoints) >= 2:
            origin = waypoints[0]
            destination = waypoints[-1]
            del waypoints[0]
            del waypoints[-1]
        else:
            print("Error: list of waypoints is too short")
            return
        
        origin = f"{origin[0]},{origin[1]}"
        destination = f"{destination[0]},{destination[1]}"
        waypoints = ["{0},{1}".format(lat, lon) for lat, lon in waypoints]

        params = {
            "origin": origin,
            "destination": destination,
            "waypoints": "|".join(waypoints),
            "key": api_key
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        total_distance = []
        if data["status"] == "OK":
            route = data["routes"][0]
            legs = route["legs"]

            for leg in legs:
                total_distance.append(leg["distance"]["value"])
        else:
            print(f"Error: {data['status']} - {data.get('error_message', 'No error message')}")

        return total_distance[::2]
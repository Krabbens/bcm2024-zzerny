import requests
import json
from vehicle import *


class Mevo:
    def __init__(self):
        pass


    def get_mevo_api(self, type):
        if (type == 'stations'):
            url = "https://gbfs.urbansharing.com/rowermevo.pl/station_information.json"
        elif (type == 'status'):
            url = "https://gbfs.urbansharing.com/rowermevo.pl/station_status.json"
        elif (type == 'bikes'):
            url = "https://gbfs.urbansharing.com/rowermevo.pl/free_bike_status.json"

        headers = {"Client-Identifier": "IDENTIFIER"}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if type == 'stations' or type == 'status':
            return data['data']['stations']
        elif type == 'bikes':
            return data['data']['bikes']


    def get_bikes(self):
        return self.get_mevo_api('bikes')
    

    
    def get_vehicles(self):
        json_obj = self.get_bikes()

        all_vehicles = []

        for bike in json_obj:
            vehicle_type = bike['vehicle_type_id']
            charge = 0
            range = bike['current_range_meters']
            lat = bike['lat']
            lon = bike['lon']

            # Tworzenie obiektu Vehicle i dodawanie do listy
            vehicle = Vehicle(vehicle_type = vehicle_type, charge = charge, lat = lat, lon = lon, brand = 'mevo', range = range)
            all_vehicles.append(vehicle)


        return all_vehicles
    

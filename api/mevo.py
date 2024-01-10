import requests
import json
from vehicle import *
from station import *

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
        data1 = self.get_bikes()
        data2 = self.get_stations(True)

        all_vehicles = []

        for bike in data1:
            if bike['is_reserved'] == True or bike['is_disabled'] == True:
                continue

            vehicle_type = bike['vehicle_type_id']
            charge = 0
            range = bike['current_range_meters']
            lat = bike['lat']
            lon = bike['lon']

            # Tworzenie obiektu Vehicle i dodawanie do listy
            vehicle = Vehicle(vehicle_type = vehicle_type, charge = charge, lat = lat, lon = lon, brand = 'mevo', range = range)
            all_vehicles.append(vehicle)

        for station in data2:
            if station.is_ebike:
                vehicle_type = 'ebike'
            elif station.is_bike:
                vehicle_type = 'bike'
            else:
                continue
            
            charge = 100
            range = 55000
            
            lat = station.location[0]
            lon = station.location[1]

            # Tworzenie obiektu Vehicle i dodawanie do listy
            vehicle = Vehicle(vehicle_type = vehicle_type, charge = charge, lat = lat, lon = lon, brand = 'mevo', range = range)
            all_vehicles.append(vehicle)


        return all_vehicles
    
    
    def get_stations(self, for_bikes = False):
        data1 = self.get_mevo_api('stations')
        data2 = self.get_mevo_api('status')

        all_stations = []

        indx = 0
        for station in data1:
            lat = station['lat']
            lon = station['lon']
            
            bikes_in_station = data2[indx]['num_bikes_available']
            docks_in_station = data2[indx]['num_docks_available']

            if station['station_id'] == data2[indx]['station_id']:
                if (bikes_in_station == 0):
                    if (for_bikes == True):
                        indx += 1
                        continue
                    empty = True
                else:
                    empty = False

                if (bikes_in_station < docks_in_station):
                    is_filled = False
                else:
                    is_filled = True
                

                vehicle_types = data2[indx]['vehicle_types_available']
                ebikes = vehicle_types[0]['count']
                bikes = vehicle_types[1]['count']

                if (ebikes > 0):
                    is_ebike = True
                else:
                    is_ebike = False
                if (bikes > 0):
                    is_bike = True
                else:
                    is_bike = False
            else:
                print("Error: Station ID mismatch")
                break

            # Tworzenie obiektu Station i dodawanie do listy
            station = Station(lat = lat, lon = lon, brand = 'mevo', filled = is_filled, is_ebike = is_ebike, is_bike = is_bike, empty = empty)
            all_stations.append(station)

            indx += 1

        return all_stations

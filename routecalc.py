from vehicle import *
from station import *
from api import *
from math import radians, sin, cos, sqrt, atan2
import time


class RouteCalc():
    def __init__(self):
        self.mevo_vehicles = []
        self.bolt_vehicles = []
        self.tier_vehicles = []

        self.mevo_stations = []
        self.tier_bolt_stations = []

        self.start_time = time.time()


    def snapshot_time(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        self.start_time = end_time
        print(f"Execution time: {elapsed_time:.6f} seconds")


    def haversine_distance(self, cords1, cords2):
        lat1 = cords1[0]
        lon1 = cords1[1]
        lat2 = cords2[0]
        lon2 = cords2[1]
        
        # Radius of the Earth in meters
        R = 6371000.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Differences in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance


    
    def get_data(self):

        self.mevo_vehicles = Mevo().get_vehicles()
        self.bolt_vehicles = Bolt().get_vehicles(init_lat = 54.362043421305046, init_lon = 18.628451433496945)   
        self.tier_vehicles = Tier().get_vehicles(init_lat = 54.362043421305046, init_lon = 18.628451433496945)

        self.mevo_stations = Mevo().get_stations()
        self.tier_bolt_stations = [] #Tier().get_stations() + Bolt().get_stations()


    def get_distances(self, vehicles, stations, location1, location2):

        distances = []
        distances2 = []

        for vehicle in vehicles:
            cords = vehicle.location
            distance1 = self.haversine_distance(cords, location1)
            distance2 = self.haversine_distance(cords, location2)

            weight = distance1 * 0.95 + distance2 * 0.05

            distances.append([cords, weight])

        for station in stations:
            cords = station.location
            distance1 = self.haversine_distance(cords, location1)
            distance2 = self.haversine_distance(cords, location2)

            weight = distance1 * 0.05 + distance2 * 0.95

            distances2.append([cords, weight])

        return distances, distances2
    

    def get_route_info(self, type, point1, point2):
        
        if (type == 'mevo'):
            vehicles = self.mevo_vehicles
            stations = self.mevo_stations
        elif (type == 'bolt'):
            vehicles = self.bolt_vehicles
            stations = self.tier_bolt_stations
        elif (type == 'tier'):
            vehicles = self.tier_vehicles
            stations = self.tier_bolt_stations

        distances1, distances2 = self.get_distances(vehicles, stations, point1, point2)

        distances1.sort(key=lambda x: x[1])
        distances2.sort(key=lambda x: x[1])

        vehicle = distances1[0][0]
        station = distances2[0][0]

        return (vehicle, station)
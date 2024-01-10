from vehicle import *
from station import *
from api import *
from math import radians, sin, cos, sqrt, atan2
import time
import google


class RouteCalc():
    def __init__(self):
        self.init_lat = 54.362043421305046
        self.init_lon = 18.628451433496945

        self.mevo_vehicles = []
        self.bolt_vehicles = []
        self.tier_vehicles = []

        self.mevo_stations = []
        self.bolt_stations = []
        self.tier_stations = []

        self.bolt_zones = []
        self.tier_zones = []

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


    def get_data_route(self, cache):
        if (cache.check_update_route()):
            self.mevo_vehicles = Mevo().get_vehicles()
            self.bolt_vehicles = Bolt().get_vehicles(init_lat = self.init_lat, init_lon = self.init_lon)   
            self.tier_vehicles = Tier().get_vehicles(init_lat = self.init_lat, init_lon = self.init_lon)

            self.mevo_stations = Mevo().get_stations()
            self.bolt_stations = [] #Tier().get_stations() + Bolt().get_stations()
            self.tier_stations = []

            cache.update_route({
                'mevo_vehicles' : self.mevo_vehicles,
                'bolt_vehicles' : self.bolt_vehicles,
                'tier_vehicles' : self.tier_vehicles,
                'mevo_stations' : self.mevo_stations,
                'bolt_stations' : self.bolt_stations,
                'tier_stations' : self.tier_stations
            })
        else:
            self.mevo_vehicles = cache.route_data['mevo_vehicles']
            self.bolt_vehicles = cache.route_data['bolt_vehicles']
            self.tier_vehicles = cache.route_data['tier_vehicles']
            self.mevo_stations = cache.route_data['mevo_stations']
            self.bolt_stations = cache.route_data['bolt_stations']
            self.tier_stations = cache.route_data['tier_stations']


    def get_data_zone(self, cache):
        if (cache.check_update_zone()):
            self.bolt_zones = Bolt().get_zones()
            self.tier_zones = [] #Tier().get_zones()

            cache.update_zone({
                'bolt_zones' : self.bolt_zones,
                'tier_zones' : self.tier_zones
            })
        else:
            self.bolt_zones = cache.zone_data['bolt_zones']
            self.tier_zones = cache.zone_data['tier_zones']
    

    def get_data(self, cache):
        self.get_data_route(cache)

        self.get_data_zone(cache)

    
    def check_which_zone(self, location):


        for zone in self.bolt_zones:
            if zone.is_inside(location):
                print(zone.type, zone.geometry)



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
    

    def validate_with_google(self, distances1, distances2, v_n, s_n):
        vehicle = []
        for i in range(v_n):
            vehicle.append(distances1[i][0])

        station = []
        for i in range(s_n):
            station.append(distances2[i][0])

        pairs = []
        for i in range(v_n):
            for j in range(s_n):
                pairs.append((vehicle[i], station[j]))

        google = Google()
        g_distances = google.get_distances(pairs)

        dist_pairs = []
        for i in range(len(g_distances)):
            dist_pairs.append([pairs[i], g_distances[i]])
        
        dist_pairs.sort(key=lambda x: x[1])

        return (dist_pairs[0][0])
    

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

        v_n = 3
        s_n = 3

        best = self.validate_with_google(distances1, distances2, v_n, s_n)

        return best
import time

class Cache:
    def __init__(self):
        
        self.route_data = {
            'update_time' : 30,
            'last_updated' : None,
            'mevo_vehicles' : [],
            'bolt_vehicles' : [],
            'tier_vehicles' : [],
            'mevo_stations' : [],
            'bolt_stations' : [],
            'tier_stations' : []
        }

        self.zone_data = {
            'update_time' : 3600,
            'last_updated' : None,
            'bolt_zones' : [],
            'tier_zones' : []
        }


    def check_update_route(self):
        if self.route_data['last_updated'] != None:
            if time.time() - self.route_data['last_updated'] <= self.route_data['update_time']:
                return False
        return True
        

    def update_route(self, data):
        self.route_data['last_updated'] = time.time()
        self.route_data['mevo_vehicles'] = data['mevo_vehicles']
        self.route_data['bolt_vehicles'] = data['bolt_vehicles']
        self.route_data['tier_vehicles'] = data['tier_vehicles']
        self.route_data['mevo_stations'] = data['mevo_stations']
        self.route_data['bolt_stations'] = data['bolt_stations']
        self.route_data['tier_stations'] = data['tier_stations']


    def check_update_zone(self):
        if self.zone_data['last_updated'] != None:
            if time.time() - self.zone_data['last_updated'] <= self.zone_data['update_time']:
                return False
        return True
    

    def update_zone(self, data):
        self.zone_data['last_updated'] = time.time()
        self.zone_data['bolt_zones'] = data['bolt_zones']
        self.zone_data['tier_zones'] = data['tier_zones']



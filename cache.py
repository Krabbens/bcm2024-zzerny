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
            'tier_bolt_stations' : []
        }

    def check_update(self):
        if self.route_data['last_updated'] != None:
            if time.time() - self.route_data['last_updated'] <= self.route_data['update_time']:
                return False
        return True
        

    def update(self, data):
        self.route_data['last_updated'] = time.time()
        self.route_data['mevo_vehicles'] = data['mevo_vehicles']
        self.route_data['bolt_vehicles'] = data['bolt_vehicles']
        self.route_data['tier_vehicles'] = data['tier_vehicles']
        self.route_data['mevo_stations'] = data['mevo_stations']
        self.route_data['tier_bolt_stations'] = data['tier_bolt_stations']



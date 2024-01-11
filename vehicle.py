class Vehicle:

    def __init__(self, vehicle_type, charge, lat, lon, brand, range = None):
        self.vehicle_type = vehicle_type
        self.charge = charge
        self.location = (lat, lon)
        self.brand = brand
        if range != None:
            self.range = range
        else:
            self.range = 0

    def __str__(self):
        return f"Vehicle(brand={self.brand}, type={self.vehicle_type}, charge={self.charge}, range={self.range}, location={self.location})"

    def getJson(self):
        coordinates = {"lat": self.location[0], "lng": self.location[1]}

        vehicle_json = {
            "type": self.vehicle_type,
            "brand": self.brand,
            "charge": self.charge,
            "range": self.range,
            "location": coordinates
        }

        return vehicle_json
    
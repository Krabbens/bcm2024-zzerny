class Zone:

    def __init__(self, geometry, type, lat, lon, brand):
        self.geometry = geometry
        self.type = type
        self.brand = brand
        self.location = (lat, lon)

    
    def __str__(self):
        return f"Zone(type={self.type}, location={self.location}, brand={self.brand})"
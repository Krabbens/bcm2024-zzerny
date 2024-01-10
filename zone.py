from shapely.geometry import Point, Polygon

class Zone:

    def __init__(self, geometry, type, lat, lon, brand):
        self.geometry = geometry
        self.type = type
        self.brand = brand
        self.location = (lat, lon)

    
    def __str__(self):
        return f"Zone(type={self.type}, location={self.location}, brand={self.brand})"
    

    def is_inside(self, location):
        return Polygon(self.geometry).contains(Point(location[0], location[1]))
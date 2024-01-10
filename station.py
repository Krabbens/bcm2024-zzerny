class Station:

    def __init__(self, lat, lon, filled, empty, is_ebike, is_bike, brand):
        self.location = (lat, lon)
        self.filled = filled
        self.empty = empty
        self.brand = brand
        self.is_ebike = is_ebike
        self.is_bike = is_bike

    
    def __str__(self):
        return f"Station(brand={self.brand}, filled={self.filled}, empty={self.empty}, is_ebike={self.is_ebike}, is_bike={self.is_bike}, location={self.location})"


class Position:
    
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def to_list(self):
        return [self.lat,self.lon]

class BluetoothStation:
    
    def __init__(self, name: str, coords: Position):
        """
        Args:
            name ([String]): name and id of the Station
            coords ([Position]): longitude and latitude of the station
        """
        self.name = name
        self.coords = coords
        
    
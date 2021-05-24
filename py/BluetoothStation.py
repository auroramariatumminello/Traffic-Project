#%%
import json
import os
from datetime import datetime
from typing import Optional, List

class Position:
    
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def to_list(self):
        return [self.lat,self.lon]

class BluetoothStation:
    
    def __init__(self, name: str, coords: Optional[Position] = Position(None, None)):
        """
        Args:
            name ([String]): name and id of the Station
            coords ([Position]): longitude and latitude of the station
        """
        self.name = name
        self.coords = coords
    
    def to_list(self):
        return [self.name] + self.coords.to_list()
    
    
      
class Measurement:
    def __init__(self, timestamp: datetime, count:int, station:BluetoothStation):
        self.timestamp = timestamp
        self.count = count
        self.station = station
    
    def to_list(self):
        return [self.timestamp,self.count,self.station.name]
        
    def get_timestamp(self):
        return self.timestamp
    
    def from_list(self, db_list:List[str]):
        return Measurement(db_list[0],db_list[1],db_list[2])



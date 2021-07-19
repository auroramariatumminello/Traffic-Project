#%%
import json
import os
from datetime import datetime
from typing import Optional, List

# Class for the geographical coordinates of stations
class Position:
    
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def to_list(self):
        return [self.lat,self.lon]

# Class to handle stations
class BluetoothStation:
    
    def __init__(self, name: str, code: Optional[int] = None ,coords: Optional[Position] = Position(None, None)):
        """
        Args:
            code ([int]): numerical label to associate to the single station (necessary for the model)
            name ([String]): name and id of the Station
            coords ([Position]): longitude and latitude of the station
        """
        self.code = code
        self.name = name
        self.coords = coords
    
    def to_list(self):
        return [self.code,self.name] + self.coords.to_list()
    
    
# Class to handle measurements, as the triple timestamp, station, number of vehicles
class Measurement:
    def __init__(self, timestamp: datetime, count:int, station:BluetoothStation):
        """
        Args:
            timestamp (datetime): datetime in which the number of vehicles is recorded
            count (int): number of vehicles passing in a given timestamp and station
            station (BluetoothStation): station where the vehicles are recorded
        """
        self.timestamp = timestamp
        self.count = count
        self.station = station
    
    def to_list(self):
        return [self.timestamp,self.count,self.station.name]
        
    def get_timestamp(self):
        return self.timestamp

    # Creation of a measurement object starting from a list of triples    
    def from_list(self, db_list:List[str]):
        return Measurement(db_list[0],db_list[1],db_list[2])



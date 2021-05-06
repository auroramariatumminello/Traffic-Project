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
    
    def __init(self, timestamp: datetime, count:int, station:BluetoothStation):
        self.timestamp = timestamp
        self.count = count
        self.station = station
        
    def to_list(self):
        return [self.timestamp,self.count,self.station]
    
    def from_list(self, db_list:List[str]):
        return Measurement(db_list[0],db_list[1],db_list[2])
    
    # Returns a list of Measurement objects from json already imported
    def from_json(self,json_data: json):
        result = []
        for element in json_data:
            if element['tname'] == "Bluetooth Count record" and element['ttype']=='Count':
                result.append(Measurement(
                    element['mvalidtime'][:19],
                    element['mvalue'],
                    element['sname']
                ))
        return result


#%%
import json
import os
import sqlite3
import mysql.connector
from datetime import datetime
from typing import Optional, List
#%%
class Position:
    
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def to_list(self):
        return [self.lat,self.lon]

class BluetoothStation:
    
    def __init__(self, name: str, coords: Optional[Position] = None):
        """
        Args:
            name ([String]): name and id of the Station
            coords ([Position]): longitude and latitude of the station
        """
        self.name = name
        self.coords = coords
      
class Measurement:
    
    def __init(self, timestamp: datetime, count:int, station:BluetoothStation):
        self.timestamp = timestamp
        self.count = count
        self.station = station
        
    def to_list(self):
        return [self.timestamp,self.count,self.station]
    
#%%

class MySQLStationManager:
    
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="bluetoothstations",
            user="root",
            password="BigData"
        )
        self.connection.autocommit = True

    def insert_measurements(self, observations: List[Measurement]):
        cursor = self.connection.cursor()
        query = "INSERT into measurement (timestamp, count, station) VALUES (%s, %s, %s)"

        for observation in observations:
            cursor.execute(query, (
                observation.timestamp,
                observation.count,
                observation.station
            ))

        cursor.close()
        
    def insert_stations(self, stations: List[BluetoothStation]):
        cursor = self.connection.cursor()
        query = "INSERT into station (name, latitude, longitude) VALUES (%s, %s, %s)"

        for station in stations:
            cursor.execute(query, (
                station.name,
                station.coords.lat,
                station.coords.lon
            ))

        cursor.close()

    # Generalize by inserting optional parameter about the station(s)
    def list_all_measurement(self):
        cursor = self.connection.cursor()
        query = "SELECT timestamp, count, station from measurement"
        cursor.execute(query)

        measurements = []
        for timestamp, count, station in cursor:
            measurements.append(Measurement(
                timestamp,
                count,
                station
            ))

        cursor.close()
        return measurements
    
    # List of all BluetoothStations in the database
    def list_all_stations(self):
        cursor = self.connection.cursor()
        query = "SELECT name, latitude, longitude from station"
        cursor.execute(query)

        stations = []
        for name, latitude, longitude in stations:
            stations.append(BluetoothStation(
                name,
                Position(latitude, longitude)
            ))

        cursor.close()
        return stations
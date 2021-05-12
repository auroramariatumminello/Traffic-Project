import json
import os
import mysql.connector
from datetime import datetime
from typing import Optional, List
from BluetoothStation import *

class MySQLStationManager:
    
    def __init__(self,user="Leonardo"):
        try:
            if user=='Aurora':
                password = "MyNewPass"
            else:
                password="banana182"
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password=password,
                port=3306,
                database="bluetoothstations",
                auth_plugin='mysql_native_password',
            )
            print("Connection established.")
        except IOError:
            print("Not able to connect. Retry.")
        self.connection.autocommit = True
        self.measurements = []
        self.stations = []

    # Need to update: ask whether the station is already in the station table
    def insert_measurements(self, observations: List[Measurement]):
        # If the station is in BluetoothStation table
        cursor = self.connection.cursor()
        query = "INSERT IGNORE into measurement (timestamp, count, station) VALUES (%s, %s, %s)"
        try:
            for obs in observations:
                cursor.execute(query, (
                    obs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    obs.count,
                    obs.station.name
                ))
            print("Data inserted.")
            cursor.close()
        except mysql.connector.IntegrityError:
            pass
         
    def insert_stations(self, stations: List[BluetoothStation]):
        cursor = self.connection.cursor()
        query = "INSERT into station (name, latitude, longitude) VALUES (%s, %s, %s)"

        for station in stations:
            if station.coords.lat == None or station.coords.lon == None:
                cursor.execute(
                    query, (
                    station.name,
                    None,
                    None))
            else:
                cursor.execute(query, (
                    station.name,
                    station.coords.lat,
                    station.coords.lon
                ))
        # print("Data inserted.")
        cursor.close()

    # Generalize by inserting optional parameter about the station(s)
    def list_all_measurement(self):
        cursor = self.connection.cursor()
        query = "SELECT * from measurement"
        cursor.execute(query)
        print("Got all measurements.")
        measurements = []
        for timestamp, count, station in cursor:
            measurements.append(Measurement(
                timestamp,
                count,
                station
            ))
        print("Finished.")
        cursor.close()
        return measurements
    
    # List of all BluetoothStations in the database
    def list_all_stations(self):
        cursor = self.connection.cursor()
        query = "SELECT * from station"
        cursor.execute(query)

        print("Got all measurements.")
        stations = []
        for name, latitude, longitude in stations:
            stations.append(BluetoothStation(
                name,
                Position(latitude, longitude)
            ))
        print("Finished.")
        cursor.close()
        return stations
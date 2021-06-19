#%%
import mysql.connector
from typing import List
import pandas as pd
from tqdm import tqdm
from BluetoothStation import BluetoothStation, Measurement, Position
#%%
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
            # print("Data inserted.")
            cursor.close()
        except mysql.connector.errors.IntegrityError:
            pass
         
    def insert_stations(self, stations: List[BluetoothStation]):
        cursor = self.connection.cursor()
        query = "INSERT IGNORE into station (name, latitude, longitude) VALUES (%s, %s, %s)"

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

#%%
class MySQLStationManagerAWS:
    
    # Connects to the database on Amazon RDS
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="traffic-db.ce2ieg6xrefy.us-east-2.rds.amazonaws.com",
            user="marshall",
            passwd="happyslashgiving",
            db="bluetoothstations",
            autocommit = True)
        print("Connection successfully created.")
            
    def get_tables(self):
        mycursor = self.connection.cursor()
        mycursor.execute("Show tables;")
        myresult = mycursor.fetchall()
        return myresult
                
    def disconnect(self):
        self.connection.close()

    # Need to update: ask whether the station is already in the station table
    def insert_measurements(self, observations: List[Measurement]):
        # If the station is in BluetoothStation table
        cursor = self.connection.cursor()
        query = "INSERT IGNORE into bluetoothstations.measurement (timestamp, count, station) VALUES (%s, %s, %s)"
        for obs in observations:
            cursor.execute(query, (
                obs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                obs.count,
                obs.station.name
            ))
        # print("Data inserted.")
        self.connection.commit()
        cursor.close()
         
    def insert_stations(self, stations: List[BluetoothStation]):
        cursor = self.connection.cursor()
        query = "INSERT into bluetoothstations.station (name, latitude, longitude) VALUES (%s, %s, %s)"

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
        self.connection.commit()
        # print("Data inserted.")
        cursor.close()

    # Generalize by inserting optional parameter about the station(s)
    def list_all_measurement(self):
        cursor = self.connection.cursor()
        query = "SELECT * from bluetoothstations.measurement"
        cursor.execute(query)
        print("Got all measurements.")
        measurements = []
        for timestamp, count, station in cursor:
            measurements.append(Measurement(
                timestamp,
                count,
                BluetoothStation(station)
            ))
        print("Finished.")
        cursor.close()
        return measurements
    
    def filter_measurements(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        measurements = cursor.fetchall()
        print("Finished.")
        print(measurements)
        cursor.close()
        return measurements
    
    # List of all BluetoothStations in the database
    def list_all_stations(self):
        cursor = self.connection.cursor()
        query = 'SELECT * from bluetoothstations.station'
        cursor.execute(query)
        stations = []
        for name, latitude, longitude in cursor:
            stations.append(BluetoothStation(
                name,
                Position(latitude, longitude)
            ))
        print("Finished.")
        print([x.to_list() for x in stations])
        cursor.close()
        return stations
    
    def get_latest_datetime(self):
        query = 'SELECT MAX(timestamp) FROM bluetoothstations.measurement;';
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()[0][0]

    def insert_csv_in_db(self, data_path):
        try:
            df = pd.read_csv(data_path)
            if df.empty:
                print("No data available yet.")
            else:
                cursor = self.connection.cursor()
                for _,row in tqdm(df.iterrows(), total=df.shape[0]):
                    sql = "INSERT INTO bluetoothstations.measurement VALUES (%s,%s,%s)"
                    cursor.execute(sql, tuple(row))
                    # the connection is not auto committed by default, so we must commit to save our changes
                self.connection.commit()
                cursor.close()
        except pd.errors.EmptyDataError:
            print("No data yet")
        

    
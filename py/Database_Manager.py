#%%
# Libraries

## DB Connectors
import mysql.connector
from pymongo import MongoClient
import yaml
import os

# Data transformation
import pandas as pd
from tqdm import tqdm

# Typing and objects
from typing import List, Optional
from BluetoothStation import BluetoothStation, Measurement, Position

config_path = "Shiny Bolzano Application/config.yml"

# MySQL DB Manager for local DB
# Note: it is necessary to dispose of local credentials
class MySQLStationManager:
    
    def __init__(self,user: str):
        try:
            with open(config_path, "r") as ymlfile:
                config = yaml.safe_load(ymlfile)['local']
            self.connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                port=config['port'],
                database=config['database'],
                auth_plugin='mysql_native_password',
            )
            print("Connection established.")
        except IOError:
            print("Not able to connect. Retry.")
        self.connection.autocommit = True
        self.measurements = []
        self.stations = []

    def insert_measurements(self, observations: List[Measurement]):
        cursor = self.connection.cursor()
        query = "INSERT IGNORE into measurement (timestamp, count, station) VALUES (%s, %s, %s)"
        try:
            for obs in observations:
                cursor.execute(query, (
                    obs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    obs.count,
                    obs.station.name
                ))
            cursor.close()
        except mysql.connector.errors.IntegrityError:
            pass
         
    def insert_stations(self, stations: List[BluetoothStation]):
        cursor = self.connection.cursor()
        next_code = cursor.execute("SELECT MAX(code) FROM station;")+1
        query = "INSERT IGNORE into station (code, name, latitude, longitude) VALUES ("+next_code+",%s, %s, %s)"

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
        cursor.close()
        return measurements
    
    # List of all BluetoothStations in the database
    def list_all_stations(self):
        cursor = self.connection.cursor()
        query = "SELECT * from station"
        cursor.execute(query)

        print("Got all measurements.")
        stations = []
        for code, name, latitude, longitude in stations:
            stations.append(BluetoothStation(
                name,
                Position(latitude, longitude)
            ))
        cursor.close()
        return stations
    
# Database manager of Amazon Web Services
class MySQLStationManagerAWS:
    
    # Connects to the database on Amazon RDS
    def __init__(self, modality = "Github"):
        if modality == "Github":
            self.connection = mysql.connector.connect(
                host=os.environ['db_host'],
                user=os.environ['db_user'],
                passwd=os.environ['password'],
                db=os.environ["dbname"],
                autocommit = True)
        else:
            with open(config_path, "r") as ymlfile:
                config = yaml.safe_load(ymlfile)['default']
            self.connection = mysql.connector.connect(
                host=config['DB_HOST'],
                user=config['DB_USER'],
                passwd=config['PASSWORD'],
                db=config["DBNAME"],
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
        self.connection.commit()
        cursor.close()
         
    # Get the last numerical code used for stations
    def get_last_code(self):
        cursor = self.connection.cursor()
        query = "SELECT MAX(code) FROM bluetoothstations.station"
        cursor.execute(query)
        return cursor.fetchall()[0][0]

    def insert_stations(self, stations: List[BluetoothStation]):
        cursor = self.connection.cursor()
        last_code = self.get_last_code()
        codes = [last_code+i for i in range(1,len(stations)+1)]
        query = "INSERT into bluetoothstations.station (name, latitude, longitude) VALUES (%s, %s, %s)"

        for i in range(len(stations)):
            if stations[i].coords.lat == None or stations[i].coords.lon == None:
                cursor.execute(
                    query, (
                    codes[i],
                    stations[i].name,
                    None,
                    None))
            else:
                cursor.execute(query, (
                    stations[i].code,
                    stations[i].name,
                    stations[i].coords.lat,
                    stations[i].coords.lon
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
        for code, name, latitude, longitude in cursor:
            stations.append(BluetoothStation(
                name,
                code,
                Position(latitude, longitude)
            ))
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
    
    def execute_query(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

class MongoDBManager():
    
    def __init__(self, modality = "Github"):
        if modality == "Github":
            with open(config_path, "r") as ymlfile:
                config = yaml.safe_load(ymlfile)['default']
            self.client = MongoClient(config['mongodb'])
        else:
            self.client = MongoClient(os.environ['MONGODB'])
        self.db = self.client.TrafficBolzano

    # Inserting model predictions inside the collection
    def insert_predictions(self,dataframe, collection = 'Predictions'):
        self.db[collection].insert_many(dataframe.to_dict('records'))            

    # Empty the collection 
    def delete_all_documents(self, collection):
        self.db[collection].delete_many({})

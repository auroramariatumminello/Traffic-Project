# %%
# Libraries
import datetime as dt
import pandas as pd
import requests
import json
import csv
import os.path
import time
from datetimerange import DateTimeRange
import pytz

# Importing scripts with objects
from BluetoothStation import *
from Database_Manager import MySQLStationManager

# %%
# Download list of bluetooth stations


def get_stations_details(url: str = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation?limit=-1&distinct=true"):
    # Requesting informations about stations
    stations = requests.get(url).json()['data']

    # Creating a list of BluetoothStation objects with regular Position
    bluetooth_stations = [BluetoothStation(station['sname'],
                                           Position(station['scoordinate']['y'],
                                                    station['scoordinate']['x']))
                          for station in stations if 'scoordinate' in station.keys()]

    # Updating the list adding BluetoothStation objects with no Position information
    bluetooth_stations = bluetooth_stations + [BluetoothStation(station['sname'])
                                               for station in stations if 'scoordinate' not in station.keys()]

    return bluetooth_stations


# %%
# Creating a MySQL Database Manager
manager = MySQLStationManager()

# Inserting the requested stations inside the station table
manager.insert_stations(get_stations_details())
# %%

# history till 2019-11-26
date_range = pd.date_range(dt.date(2013, 1, 1), dt.date(
    2021, 4, 25)-dt.timedelta(days=1), freq='d')
date_range = [date.strftime("%Y-%m-%d") for date in date_range]
# %%

# URL to request vehicle detection in Bluetooth Stations
data_url = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation/%2A/{}/{}?limit=-1&distinct=true&timezone=UTC"
data_format = "{}-{}-{}T{}%3A{}%3A{}.000%2B0000"  # YYYY-mm-ddTHH:MM:SS

# %%


def get_data_of_day(url, sdate, edate, filename=None):
    try:
        start = time.time()
        if (dt.datetime(2019, 11, 26, tzinfo=pytz.UTC) <= sdate <= dt.datetime.now(tz=pytz.UTC)) or (dt.datetime(2019, 11, 26, tzinfo=pytz.UTC) <= edate <= dt.datetime.now(tz=pytz.UTC)):
            # For limited requests (every hour)
            req = requests.get(url.format(data_format.format(sdate.year, 
                                                             sdate.strftime("%m"), 
                                                             sdate.strftime("%d"),
                                                             sdate.strftime("%H"),
                                                             sdate.strftime("%M"),
                                                             sdate.strftime("%S")),
                                          data_format.format(edate.year,
                                                             edate.strftime("%m"),
                                                             edate.strftime("%d"),
                                                             edate.strftime("%H"),
                                                             edate.strftime("%M"),
                                                             edate.strftime("%S"))))
        else:
            # For ordinary requests
            req = requests.get(url.format(sdate, edate))
        day_data = req.json()["data"]
        results = Measurement().from_json(day_data)
        if filename != None:
            results = [x.to_list() for x in results]
            headers = ["Timestamp", "Count", "Station"]
            pd.DataFrame(results, columns=headers).to_csv(filename,
                                                          mode='a',
                                                          index=False,
                                                          header=False)
        print(time.time()-start)
        return results
    except ValueError:
        # Possible error of gateway, retry after 1 minute
        print("Gateway Time-out error")
        time.sleep(60)
        get_data_of_day(url, sdate, edate, filename)


# %%

# Collecting data from january 2018 to November 2019
date_range_2019 = pd.date_range(dt.date(2018, 1, 1), dt.date(
    2019, 11, 26)-dt.timedelta(days=1), freq='d')
date_range_2019 = [date.strftime("%Y-%m-%d") for date in date_range_2019]
for i in (range(len(date_range_2019)-1)):
    print("Saving "+str(date_range_2019[i]))
    get_data_of_day(url,
                    date_range_2019[i],
                    date_range_2019[i+1],
                    filename='2019.csv')


# %%
# Datetime range
time_range = DateTimeRange("2019-11-26T00:00:00.000+0000",
                           "2020-01-02T00:00:00.000+0000")
time_range = [value for value in time_range.range(dt.timedelta(hours=1))]
# %%
manager = MySQLStationManager()
for i in range(len(time_range)-1):
    sdate = time_range[i]
    edate = time_range[i+1]
    #get_data_of_day(url, sdate, edate)
    manager.insert_measurements(get_data_of_day(url, sdate, edate))

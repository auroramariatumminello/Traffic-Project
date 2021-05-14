# %%
# Libraries
import datetime as dt
import datetimerange
import pandas as pd
import requests
import json
import csv
import os.path
import time
from datetimerange import DateTimeRange
import pytz
import tqdm

# Importing scripts with objects
from BluetoothStation import *
from Database_Manager import *
#%%
# Creating a MySQL Database Manager
manager = MySQLStationManager("Aurora")

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
# Inserting the requested stations inside the station table
# manager.insert_stations(get_stations_details())
# %%

# URL to request vehicle detection in Bluetooth Stations
data_url = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation/%2A/{}/{}?limit=-1&distinct=true&timezone=UTC"
data_format = "{}-{}-{}T{}%3A{}%3A{}.000%2B0000"  # YYYY-mm-ddTHH:MM:SS

# %%
def get_data_of_day(url, sdate, edate, filename=None):
    try:
        start = time.time()
        #if (dt.datetime(2019, 11, 26, tzinfo=pytz.UTC) <= sdate <= dt.datetime.now(tz=pytz.UTC)) or (dt.datetime(2019, 11, 26, tzinfo=pytz.UTC) <= edate <= dt.datetime.now(tz=pytz.UTC)):
        #    # For limited requests (every hour)
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
        #else:
            # For ordinary requests
        #    req = requests.get(url.format(sdate.isoformat(), edate.isoformat()))
        day_data = req.json()["data"]
        results = from_json_to_list(day_data)
        headers = ["Timestamp", "Count", "Station"]
        df = pd.DataFrame(results, columns=headers).groupby(['Timestamp','Station'],as_index=False).sum()
        
        # From dataframe to Measurements list
        results = [Measurement(df.iloc[i, 0],
                               int(df.iloc[i, 2]),
                               BluetoothStation(df.iloc[i, 1])) for i in range(len(df))]
        # print(time.time()-start)
        if filename != None:
            df.to_cv(filename,
                     mode='a',
                     index=False,
                     header=False)
        return results
    except (ValueError,KeyError):
        # Possible error of gateway, retry after 1 minute
        print("Gateway Time-out error")
        time.sleep(60)
        get_data_of_day(url, sdate, edate, filename)


def from_json_to_list(json_data: json):
    result = []
    for element in json_data:
        if element['tname'] == "Bluetooth Count record" and element['ttype'] == 'Count':
            m = [datetime.strptime(element['mvalidtime'][:19], '%Y-%m-%d %H:%M:%S'),
                 element['mvalue'],
                 element['sname']]
            result.append(m)
    return result

# Returns a list of Measurement objects from json already imported
def from_json_to_measurement(json_data: json):
    result = []
    for element in json_data:
        if element['tname'] == "Bluetooth Count record" and element['ttype']=='Count':
            m = Measurement(datetime.strptime(element['mvalidtime'][:19],'%Y-%m-%d %H:%M:%S'),
                            element['mvalue'],
                            BluetoothStation(element['sname']))
            result.append(m)
    return result

#%%
# DATE RANGE
date_range = DateTimeRange("2018-10-30T01:40:00.000+0000",
                           "2019-11-26T00:00:00.000+0000",)
date_range = [value for value in date_range.range(dt.timedelta(hours=1))]


# %%
def get_data_in_range(date_range,url=data_url): 
    manager = MySQLStationManager("Aurora")
    for i in tqdm.tqdm(range(len(date_range)-1)):
        sdate = date_range[i]
        edate = date_range[i+1]
        try:
            manager.insert_measurements(get_data_of_day(url, sdate, edate))
        except mysql.connector.errors.IntegrityError:
            print("Already in the DB")

# %%
get_data_in_range(date_range)
# %%

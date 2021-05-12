# %%
# Libraries
import datetime as dt
import pandas as pd
import requests
import json
import csv
import os.path
import time
import pytz
import tqdm

# Importing scripts with objects
from BluetoothStation import *
from Database_Manager import *
#%%
# Creating a MySQL Database Manager
manager = MySQLStationManager("Aurora")
# %%

# URL to request vehicle detection in Bluetooth Stations
data_url = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation/%2A/{}/{}?limit=-1&distinct=true&timezone=UTC"
data_format = "{}-{}-{}T{}%3A{}%3A{}.000%2B0000"  # YYYY-mm-ddTHH:MM:SS

# %%
def get_data_of_day(url, sdate, edate, filename=None):
    try:
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
        
        day_data = req.json()["data"]
        results = from_json_to_list(day_data)
        results = results
        if filename != None:
            df.to_cv(filename,
                     mode='a',
                     index=False,
                     header=False)
        return results
    except ValueError:
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


#%%
# DATE RANGES

# Date range from 01-01-2013 to 26-11-2019 (in days)
old_date_range = DateTimeRange("2021-04-01T00:00:00.000+0000","2021-12-31T00:00:00.000+0000")
old_date_range = [value for value in old_date_range.range(dt.timedelta(hours=1))]

# Datetime range from 26-11-2019 00:00:00 to nowadays (in hours)
new_date_range = DateTimeRange("2019-11-26T00:00:00.000+0000",
                               "2020-01-01T00:00:00.000+0000")
new_date_range = [value for value in new_date_range.range(dt.timedelta(hours=1))]

# %%
#   TODO: Progress bar
def get_data_in_range(date_range,url=data_url):
    manager = MySQLStationManager("Aurora")
    for i in tqdm.trange(len(date_range)-1):
        sdate = date_range[i]
        print("Saving "+str(sdate))
        edate = date_range[i+1]
        manager.insert_measurements(get_data_of_day(url, sdate, edate))

# %%
get_data_in_range(old_date_range)
# %%
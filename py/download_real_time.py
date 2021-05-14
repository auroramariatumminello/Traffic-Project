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
from datetimerange import DateTimeRange
# %%
# URL to request vehicle detection in Bluetooth Stations
data_url = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation/%2A/{}/{}?limit=-1&distinct=true&timezone=UTC"
data_format = "{}-{}-{}T{}%3A{}%3A{}.000%2B0000"  # YYYY-mm-ddTHH:MM:SS

# %%
def get_data_of_day(url, sdate, edate, filename=None):
    try:
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
    except ValueError:
        # Possible error of gateway, retry after 1 minute
        print("Gateway Time-out error")
        time.sleep(60)
        get_data_of_day(url, sdate, edate, filename)


def from_json_to_list(json_data: json):
    result = []
    for element in json_data:
        if element['tname'] == "Bluetooth Count record" and element['ttype'] == 'Count':
            m = [dt.strptime(element['mvalidtime'][:19], '%Y-%m-%d %H:%M:%S'),
                 element['mvalue'],
                 element['sname']]
            result.append(m)
    return result


#%%
# %%
def get_data_in_range(date_range,url=data_url):
    db = MySQLStationManager("Aurora")
    for i in tqdm.trange(len(date_range)-1):
        sdate = date_range[i]
        print("Saving "+str(sdate))
        edate = date_range[i+1]
        for row in get_data_of_day(url, sdate, edate):
            db.putItem(row)

# %%
get_data_in_range(date_range)
# %%
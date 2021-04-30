# %%
import datetime as dt
import pandas as pd
import requests
import json
import csv
import os.path
import time
from datetimerange import DateTimeRange
import pytz
# %%
# history till 2019-11-26
date_range = pd.date_range(dt.date(2013, 1, 1), dt.date(
    2021, 4, 25)-dt.timedelta(days=1), freq='d')
date_range = [date.strftime("%Y-%m-%d") for date in date_range]
# %%
url = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation/%2A/{}/{}?limit=-1&distinct=true&timezone=UTC"

data_format = "{}-{}-{}T{}%3A{}%3A{}.000%2B0000"  # YYYY-mm-ddTHH:MM:SS
# %%


def from_json_to_list(data):
    result = []
    for element in data:
        if element['tname'] == "Bluetooth Count record" and element['ttype']=='Count':
            result.append([
                element['mvalidtime'][:19],
                element['mvalue'],
                element['sname']
            ])
    return result


def get_data_of_day(url, sdate, edate, filename="history.csv"):
    try:
        start = time.time()
        if (dt.datetime(2019, 11, 26, tzinfo=pytz.UTC) <= sdate <= dt.datetime.now(tz=pytz.UTC)) or (dt.datetime(2019, 11, 26, tzinfo=pytz.UTC) <= edate <= dt.datetime.now(tz=pytz.UTC)):
            req = requests.get(url.format(data_format.format(sdate.year,
                                                             sdate.strftime(
                                                                 "%m"),
                                                             sdate.strftime(
                                                                 "%d"),
                                                             sdate.strftime(
                                                                 "%H"),
                                                             sdate.strftime(
                                                                 "%M"),
                                                             sdate.strftime("%S")),
                                          data_format.format(edate.year,
                                                             edate.strftime(
                                                                 "%m"),
                                                             edate.strftime(
                                                                 "%d"),
                                                             edate.strftime(
                                                                 "%H"),
                                                             edate.strftime(
                                                                 "%M"),
                                                             edate.strftime("%S"))))
        else:
            req = requests.get(url.format(sdate, edate))
        day_data = req.json()["data"]
        results = from_json_to_list(day_data)
        headers = ["Timestamp", "Count", "Station"]
        pd.DataFrame(results, columns=headers).to_csv(filename,
                                                      mode='a',
                                                      index=False,
                                                      header=False)
        print(time.time()-start)
        return results
    except ValueError:
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
time_range = DateTimeRange("2019-12-31T00:00:00.000+0000", 
                           "2020-01-01T00:00:00.000+0000")
time_range = [value for value in time_range.range(dt.timedelta(hours=1))]
#%%
for i in range(len(time_range)-1):
    sdate = time_range[i]
    edate = time_range[i+1]
    get_data_of_day(url, sdate, edate,filename="test.csv")
# %%

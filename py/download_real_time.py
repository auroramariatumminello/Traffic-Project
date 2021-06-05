# %%
# Libraries
import datetime as dt
import pandas as pd
import requests
import json
import os.path
import os
import time
import tqdm
from datetimerange import DateTimeRange
from Database_Manager import MySQLStationManagerAWS
from BluetoothStation import *
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
        headers = ["Timestamp", "Count", "Station"]
        df = pd.DataFrame(results, columns=headers).groupby(['Timestamp','Station'],as_index=False).sum().reset_index().drop('index',axis=1)
        df = df.reindex(columns=headers)
        return df
    except ValueError:
        # Possible error of gateway, retry after 1 minute
        print("Gateway Time-out error")
        time.sleep(60)
        get_data_of_day(url, sdate, edate, filename)

def convert_df_to_list_of_measurements(df):
    # From dataframe to Measurements list
    results = [Measurement(df.iloc[i, 0],
                            int(df.iloc[i, 2]),
                            BluetoothStation(df.iloc[i, 1])) for i in range(len(df))]
    return results
    
# Convert json data to list with timestamp, count and station
def from_json_to_list(json_data: json):
    result = []
    for element in json_data:
        if element['tname'] == "Bluetooth Count record" and element['ttype'] == 'Count':
            m = [dt.datetime.strptime(element['mvalidtime'][:19], '%Y-%m-%d %H:%M:%S'),
                 element['mvalue'],
                 element['sname']]
            result.append(m)
    return result


# %%
def get_missing_data(url=data_url, data_path = 'data/latest_data.csv'):
    # Manager to communicate with MySQL on EC2
    db = MySQLStationManagerAWS()
    
    # Datetime of the last data gathered
    last_date = db.get_latest_datetime()
    print("Last time you downloaded: "+str(last_date))
    
    # Creating date range from last time we updated the db till now
    date_range = DateTimeRange(last_date+dt.timedelta(minutes=1),
                               dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_range = [value for value in date_range.range(dt.timedelta(hours=1))]
    print("Downloading data...")
    # Get data for each hour
    for i in tqdm.trange(len(date_range)-1):
        sdate = date_range[i]
        edate = date_range[i+1]
        
        # Downloading data and saving it in pickle format
        msmt = get_data_of_day(url, sdate, edate)
        # saves data in a temporary csv
        if i==0:
            msmt.to_csv(data_path, header=True, index=False)
        else:
            msmt.to_csv(data_path, mode='a', header=False, index=False) 

    # Inserting data from csv inside the database 
    print("Inserting data inside the database...")
    db.insert_csv_in_db(data_path)
    print("Done.")
    os.remove(data_path)
    
# %%
while True:
    get_missing_data()
    time.sleep(60*10)

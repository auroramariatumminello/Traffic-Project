#%%
import datetime as dt
import pandas as pd
import requests
import json
import csv
import os.path
import time
#%%
date_range = pd.date_range(dt.date(2013,1,1),dt.date(2021,4,25)-dt.timedelta(days=1),freq='d')
date_range = [date.strftime("%Y-%m-%d") for date in date_range]
#%%
url = "https://mobility.api.opendatahub.bz.it/v2/flat%2Cnode/BluetoothStation/%2A/{}/{}?limit=-1&distinct=true&timezone=UTC"
# %%

def from_json_to_list(data):
    result = []
    for element in data:
        result.append([
            element['mvalidtime'][:19],
            element['mvalue'],
            element['sname']
        ])
    return result

def get_data_of_day(url,sdate,edate,filename="history.csv"):
    try:
        start = time.time()
        req = requests.get(url.format(sdate,edate))
        day_data = req.json()["data"]
        results = from_json_to_list(day_data)
        headers = ["Timestamp","Count","Station"]
        pd.DataFrame(results,columns=headers).to_csv(filename, 
                                                    mode='a',
                                                    index=False,
                                                    header=False)
        print(time.time()-start)
        return results
    except ValueError :
        print("Gateway Time-out error")
        time.sleep(60)
        get_data_of_day(url, sdate, edate,filename)

# %%
date_range_2019 = pd.date_range(dt.date(2019,11,26),dt.date(2020,1,1)-dt.timedelta(days=1),freq='d')
date_range_2019 = [date.strftime("%Y-%m-%d") for date in date_range_2019]
for i in (range(len(date_range_2019)-1)):
    print("Saving "+str(date_range_2019[i]))
    get_data_of_day(url, 
                    date_range_2019[i], 
                    date_range_2019[i+1],
                    filename='2019.csv')
    
    
# %%
#%%
import requests 
import json
import time

#%%
url = "https://mobility.api.opendatahub.bz.it/v1/bluetooth/rest/get-newest-record?station="

#%%
def get_all_stations():
    req = requests.get("https://mobility.api.opendatahub.bz.it/v1/bluetooth/rest/get-stations")
    stations = json.loads(req.text)
    return stations

stations = get_all_stations()
# %%
def get_latest_data(url, station):
    new_url = url+station
    req = requests.get(new_url)
    results = req.json()
    return [station, results['timestamp'],results['value']]

for station in stations:
    print(get_latest_data(url,station))
# %%
def save_data(data, filename):
    try:
        f = open(filename,"a")
    except IOError:
        f = open(filename,"w")
    f.writelines("%s\n" % station for station in data)
    print("Data saved.")   
    
while(True):
    print("Loading...")
    stations = get_all_stations()
    print("Saving...")
    save_data(stations,"bluetooth.csv")
    time.sleep(60)
    print("Waiting 60 sec...")

# %%

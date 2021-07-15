# %%
# Libraries

# Model
from tensorflow import keras

# Data Transformation
from datetime import timedelta
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

import Database_Manager
# %%

# 1. Selecting the most recent data inside the db
db = Database_Manager.MySQLStationManagerAWS()
last_date = db.get_latest_datetime()
start_date = (last_date-timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
data = pd.DataFrame(db.execute_query('SELECT * FROM bluetoothstations.measurement WHERE timestamp >= \"'+start_date+'\";'),columns=['timestamp','count','station'])
first_date = db.execute_query("SELECT MIN(timestamp) FROM bluetoothstations.measurement;")[0][0]

# 2. Convert timestamp to int
data['timestamp'] = [(int(x.timestamp())-int(first_date.timestamp())) for x in data['timestamp']]


# 3. Data preprocessing
# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

#%%

# 4. Create a list of dataframe for each station
stations = db.list_all_stations()
stations = [x.to_list()[:2] for x in stations]
codes = dict()
for station in stations:
    codes[station[1]] = station[0]
data['station'] = [codes[x] for x in data['station']]
data_per_station = [data[data['station']== x] for x in range(1,len(stations)+1)]
data = data[['count','timestamp','station']]
#%%

# 5. Preprocessing data considering 5 temporal stages of data
def create_model_dataset(dataframes):
	scaler = StandardScaler()
	final_df = pd.DataFrame()
	for df in dataframes:
		if not df.empty:
			count = scaler.fit_transform(df['count'].values.astype('float32').reshape(1,-1).T)
			scaled = np.concatenate((count,df['station'].values.astype('float32').reshape(1,-1).T), axis=1)
			
   			# frame as supervised learning
			reframed = series_to_supervised(scaled, 5, 1)
			reframed.drop(['var2(t)'], axis=1, inplace=True)
			final_df = final_df.append(reframed)
	return final_df.reset_index(drop=True), scaler

#%%
train, scaler = create_model_dataset(data_per_station)
train = train.values
#%%
# %%
# 6. Dividing X and y
train_X = train[:,:-1]
train_y = train[:,-1]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))

# %%

# 7. Importing the pretrained model
model = keras.models.model_from_json(open("data/model/model.json",'r').read())
model.load_weights("data/model/model.h5")

# 8. Predicting the outcome for the latest timestamp
yhat = model.predict(train_X)
predictions = scaler.inverse_transform(yhat)

indexes = []
i = 1
for j in range(len(train[:,1])):
    if train[j,1]>i:
        indexes.append(j-1)
        i = i+1
indexes.append(-1)          

# Keeping only the actual final predictions for each station
preds = predictions.ravel()[indexes]
print(preds)

# 9. Creating the output csv
output = pd.DataFrame()
output['count'] = [max(int(np.round(x,0)),0) for x in preds]
output['station'] = codes.keys()
output['timestamp'] = [(last_date+timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")] * len(preds)

output.to_csv("data/prediction.csv",index=False)
print("Predictions saved")
# 10. Overriding the past model with updated weights
model_json = model.to_json()
with open("data/model/model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("data/model/model.h5")
print("Model saved.")
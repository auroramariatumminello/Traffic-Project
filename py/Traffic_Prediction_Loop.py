# %%
# Libraries

# Model
from pandas.core.frame import DataFrame
from Database_Manager import MongoDBManager
from tensorflow import keras
from typing import Optional

# Data Transformation
from datetime import timedelta, datetime
import time
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

import Database_Manager
# %%
# 1. Access latest data
def initialize_dataset(last_date):
    # Selecting the most recent data inside the db
    db = Database_Manager.MySQLStationManagerAWS()
    start_date = (last_date-timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")
    data = pd.DataFrame(db.execute_query('SELECT * FROM bluetoothstations.measurement WHERE timestamp >= \"'+start_date+'\";'),columns=['timestamp','count','station'])
    return data, db

# 2. Prepare the dataset by creating a dataframe for each station
def prepare_dataset_for_sequential(dataframe, last_date, db):
    data = dataframe.copy()
    
    # Create a list of dataframe for each station
    stations = db.list_all_stations()
    stations = [x.to_list()[:2] for x in stations]
    codes = dict()
    for station in stations:
        codes[station[1]] = station[0]
    data['station'] = [codes[x] for x in data['station']]
    data_per_station = [data[data['station']== x] for x in range(1,len(stations)+1)]
    data = data[['count','timestamp','station']]
    return data_per_station, codes

# 3. Preprocessing data considering 5 temporal stages of data, grouped per station
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

# 4. Convert series to supervised learning
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


# 5. Dividing X and y
def data_split(data):
    train_X = data[:,:-1]
    train_y = data[:,-1]
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    return train_X, train_y

# 6. Importing the pretrained model
def model_import(path = "data/model"):
    model = keras.models.model_from_json(open(path+"/model.json",'r').read())
    model.load_weights(path+"/model.h5")
    return model

# 7. Predicting the outcome for the latest timestamp
def obtain_prediction_dataframe(model, X, data, scaler, station_codes):
    
    # Prediction
    yhat = model.predict(X)
    # Inverse scaling to get actual results
    predictions = scaler.inverse_transform(yhat)

    # Consider only the last prediction for each station,
    # since other ones are predictions on a timestamp we already know
    indexes = dict()
    for label in station_codes.values():
        indexes[label] = 0
    i = 1
    for j in range(len(data[:,1])-1):
        if data[j,1]>i:
            indexes[data[j-1,1]] = predictions.ravel()[j-1]
            i = i+1
        
    indexes[list(indexes.keys())[-1]] = predictions.ravel()[-1]
    preds = indexes.values()
    # Creating the output csv
    output = pd.DataFrame()
    output['count'] = [max(int(np.round(x,0)),0) for x in preds]
    output['station'] = station_codes.keys()
    # Considering the prediction as the result of the sequential timestamp,
    # 10 minutes after the latest one
    output['timestamp'] = [(last_date+timedelta(minutes=10))] * len(preds)
    return output

# 8. Overriding the past model with updated weights
def update_model(model, path = "data/model"):
    model_json = model.to_json()
    with open(path+"/model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(path+"/model.h5")

# 9. Inserting data inide the MongoDB database
def insert_inside_db(dataframe):
    mongodb = MongoDBManager()
    mongodb.insert_predictions(dataframe)
    print("Predictions saved inside MongoDB")

#%%
i=1
predictions = None
last_date = Database_Manager.MySQLStationManagerAWS().get_latest_datetime()
# Get initial data (latest data inside the MySQL db)
data, db = initialize_dataset(last_date)

# Enter inside the loop:
while(i<=60):
    
    # 1. Create data for the model and eventually appending latest data with predictions for new predictions
    data = pd.concat([data,predictions])
    data_per_station, codes = prepare_dataset_for_sequential(data, last_date, db)
    test, scaler = create_model_dataset(data_per_station)
    test = test.values
    test_X, test_y = data_split(test)
    
    # 2. Model import
    model = model_import()
    
    # 3. Predictions
    predictions = None
    predictions = obtain_prediction_dataframe(model, test_X, test, scaler, codes)

    # Reordering columns before appending
    predictions = predictions[['timestamp','count','station']]
    predictions['timestamp'] = [x.strftime("%Y-%m-%d %H:%M:%S") for x in predictions['timestamp']]
    # 4. Updating the model
    update_model(model)
    
    # 5. Inserting predictions inside the db
    insert_inside_db(predictions)
    predictions['timestamp'] = [datetime.strptime(x,"%Y-%m-%d %H:%M:%S") for x in predictions['timestamp']]
    
    # 6. Get last date of "training" samples for next iteration
    last_date = predictions.timestamp[0]
    i = i+1
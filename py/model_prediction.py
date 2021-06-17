#%%
import pandas as pd
import numpy as np
df = pd.read_csv("../data/2021-06-10.csv")

#%%
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

#%%
df.timestamp = pd.to_datetime(df.timestamp,format = "%Y-%m-%d %H:%M:%S")

#%%
def timeseriesToSupervised(data,n,h):
    x,y = [],[]
    for i in range(len(data)-n-h+1):
        x.append(df.iloc[i:(i+n),[0,2]])
        y.append(df.iloc[i+h+n-1,1])
    
    return np.array(x),np.array(y)
#%%
h = 1
n = 2
#%%

# Train and test split
from datetime import datetime, timedelta

latest_timestamp = max(df['timestamp'])
test = df[df["timestamp"] >= latest_timestamp-timedelta(hours=1)]
train = df[df["timestamp"] < latest_timestamp-timedelta(hours=1)]
# %%
trainX,trainy = timeseriesToSupervised(train,n,h)
testX,testy = timeseriesToSupervised(test,n,h)
#%%
from sklearn.preprocessing import LabelEncoder

LE = LabelEncoder()
df[['station_code']] = LE.fit_transform(df[['station']])
# %%
[x.toordinal() for x in df.timestamp]

# %%
[x for x in df.iloc[:10,0]]
# %%
from datetimerange import DateTimeRange
#%%
df[['time_code']] = LE.fit_transform(df[['timestamp']])
# %%
df
# %%
len(set(df.timestamp))

# %%
!pip install tensorflow


# %%
timeseriesToSupervised(df.iloc[:10],3,h)

# %%
print(df)


# %%

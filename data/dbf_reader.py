
#%%
!pip install dbf
#%%
from dbfread import DBF
from simpledbf import Dbf5

filepath = 'ITH10/roadlinks_ITH10.dbf'
    
#%%
import dbf
import pandas as pd

table = dbf.Table(filename=filepath)
table.open(dbf.READ_ONLY)
#%%
df = pd.DataFrame(table)
table.close()

print(df)
# %%

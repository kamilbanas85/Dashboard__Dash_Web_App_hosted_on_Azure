import numpy as np
import pandas as pd
import datetime
# import feather

import pyodbc
from retry import retry


#%%

def Download_And_Process_Data(Authenication: str = 'trusted-azure',\
                              returnData: bool = False,\
                              FolderWithData: str = '\\'):
   # Authenication =  'trusted'  or  'password'  or  'trusted-azure'


   # Define query
   Sql_query = """
       SELECT   *
       FROM [dbo].[Texas_Electricity_Demand2]
   """
   
   # Download data from to DB
   from Download_Data_From_sql_DB import Download_Data_From_AzureDB
   Demand_Electricity_Texas_Raw = Download_Data_From_AzureDB( Sql_query, Authenication)


   # Basic Process Data
   Demand_Electricity_Texas = Demand_Electricity_Texas_Raw\
                                   .assign(Date = lambda x: pd.to_datetime(x['Date']))\
                                   .set_index('Date')
   
   # Define second variable
   Demand_Electricity_Texas = Demand_Electricity_Texas\
          .assign( Demand_02 = lambda x: x['Demand'].shift(24*30*3).resample('w').mean()/2 )\
          .interpolate(method='ffill').interpolate(method='bfill')\
          .loc['2016':]
                
   Demand_Electricity_Texas.columns = ['Data_01', 'Data_02']

   ### Create Forecast
   
   Demand_Electricity_Texas_Forecast = \
               pd.concat(  [ Demand_Electricity_Texas.iloc[[-1],:], 
                             pd.DataFrame(index = [Demand_Electricity_Texas.index[-1] + pd.Timedelta(days=180)]) ] )\
               .asfreq('H').interpolate(method = 'ffill')
   

   Demand_Electricity_Texas_Forecast = Demand_Electricity_Texas_Forecast.add_suffix('__Forecast')
     
    
    
   # Return Data If Require
   if returnData:
       return (Demand_Electricity_Texas, Demand_Electricity_Texas_Forecast)
   else:
       return None
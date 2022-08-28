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
   
                
   Demand_Electricity_Texas.columns = ['Data_01']

 
    
   # Return Data If Require
   if returnData:
       return Demand_Electricity_Texas
   else:
       return None
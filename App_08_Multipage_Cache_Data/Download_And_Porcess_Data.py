import numpy as np
import pandas as pd
import datetime
# import feather
import time
#import pyodbc
#from retry import retry

#%%

# import os
# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)


#%%

def Download_And_Process_Data(Authenication: str = 'trusted-azure',\
                              returnData: bool = False,\
                              FolderWithData: str = '\\'):
   # Authenication =  'trusted'  or  'password'  or  'trusted-azure'

   

   # Define query
   Sql_query = """
       SELECT   *
       FROM BTCUSD.Price_30m
   """
   
   
   History = pd.DataFrame()
   
   # Download Bitcoin data from DB
   from Download_Data_From_sql_DB import Download_Data_From_localDB_Alchemy
   try:
       
       History = Download_Data_From_localDB_Alchemy( Sql_query, Authenication)
       # Basic Process Data
       History.set_index('DateTimeUTC', inplace = True)  
   except:
       print('Problem with DB')
       pass
   


   ########################################################################
   ########################################################################
   #%% Download lack of Bitcoin Data

   from DownloadBTCdata_API_binance import DownloadBTCdata
   from Download_Data_From_sql_DB import Save_Data_to_localDB_Alchemy
   
   if History.shape[0] != 0:
       Start_DateTime =  History.index[-1]
       Start_DateTime_str = Start_DateTime.strftime("%Y-%m-%d, %H:%M:%S")
   else:
       Start_DateTime_str = '2016-01-01'
       

   HistoryLack = DownloadBTCdata(Start_DateTime_str)
   HistoryLack = HistoryLack.query('dateTimeUTC != openTimeUTC')

   HistoryLack = HistoryLack.drop(columns = 'openTimeUTC')\
                            .sort_values('dateTimeUTC')
   ########################################################################
   ########################################################################
   #%% Save lack data to DB
   
   try:
       Save_Data_to_localDB_Alchemy(HistoryLack, Authenication = Authenication )
   except:
       print('Proble with DB - save data')
       pass

   #%% HistoryLack - Remove duplicates on Index - ClosingTime and sort values

   # dupl = HistoryLack[HistoryLack.index.duplicated(keep=False)]


   
   HistoryTotal_30m = pd.concat([History,HistoryLack])
   
   HistoryTotal_1d = HistoryTotal_30m.copy()\
                        .resample('d').agg({'open': 'first', 'close': 'last','high':'max','low':'min'})
   
   # remove last no full day
   HistoryTotal_1d = HistoryTotal_1d[:-1] 
   
   
   # calculate Return
   HistoryTotal_1d['Return'] = 100 * (HistoryTotal_1d[['close']].pct_change())

   
   #%% RETURN DATA

   DataToRetrun = {  'HistoryTotal_30m':HistoryTotal_30m\
                    ,'HistoryTotal_1d' :HistoryTotal_1d
                  }
   
   
   # Return Data If Require
   if returnData:
       return DataToRetrun
   else:
       return None
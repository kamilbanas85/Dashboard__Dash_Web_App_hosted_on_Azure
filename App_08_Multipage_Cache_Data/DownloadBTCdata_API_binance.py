import numpy as np
import pandas as pd
import datetime
import os

from binance.client import Client


#%%

# Initialize the client 
###### classic
# api_key = 'xxx'
# api_secret = 'yyy'

####### or save api key and secter as env veriabe:
### Windows in cmd:
# set binance_api="your_api_key_here"
# set binance_secret="your_api_secret_here"
### Linux:
# export binance_api="your_api_key_here"
# export binance_secret="your_api_secret_here"


##############################################
### StartDate. Str or int:
# Start_Timestamp_ms = int(round(Start_DateTime.timestamp() * 1000, 0))
# Start_DateTime_str = '2022-01-01T00:00:00 UTC'



def DownloadBTCdata(StartDate, interval = '30m'):

    # Initialize the client 
    api_key = os.environ.get('binance_api')
    api_secret = os.environ.get('binance_secret')
    
    client = Client(api_key, api_secret)
    
    
    symbol = "BTCUSDT"
    #interval = "30m"
    # Start_DateTime = data.index[-1]
    # Start_Timestamp_ms = int(round(Start_DateTime.timestamp() * 1000, 0))


    History = client.get_historical_klines(symbol, interval, start_str = StartDate)


    # Process Data


    HistoryDF = pd.DataFrame(History)

     # create colums name
    HistoryDF.columns = ['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']
                
    # Conver 'close_time' into datetime object, round to min and set in as index
    HistoryDF = HistoryDF.assign(dateTimeUTC = lambda x: pd.to_datetime(x['close_time'], unit = 'ms'),\
                                 openTimeUTC = lambda x: pd.to_datetime(x['open_time'], unit = 'ms'))\
                         .assign(dateTimeUTC = lambda x: x['dateTimeUTC'].dt.round('1min'),
                                 openTimeUTC = lambda x: x['openTimeUTC'].dt.round('1min') )\
                         .set_index('dateTimeUTC')\
                         .drop(columns=['open_time', 'close_time', 'ignore'])

    # convert collumns to numeric
    NoNumCol = 'openTimeUTC'
    for col in HistoryDF.loc[ :, HistoryDF.columns != NoNumCol ].columns:
        HistoryDF.loc[:,col] = pd.to_numeric( HistoryDF.loc[:,col], errors='coerce' )

    # Select Closed Price Only
    DateTimeNowUTC = datetime.datetime.utcnow()
    HistoryDF = HistoryDF[:DateTimeNowUTC]
    
    return HistoryDF

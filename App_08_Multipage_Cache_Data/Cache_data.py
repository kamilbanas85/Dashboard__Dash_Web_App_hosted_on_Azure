import json
import datetime
import pandas as pd

import dash
from flask_caching import Cache

#%%


# def create_new_cache():
#     try:
#         app = dash.get_app()
#         server = app.server
#     except Exception:
#         # Ok if importing via repl
#         #logger.warning("Dash app not set first, not caching across dash server")
#         from flask import Flask

#         server = Flask(__name__)
#         cache = Cache(
#         app=server,
#         config=CACHE_CONFIG,
#     )
#     with server.app_context():
#         cache.clear()
#     return cache


# cache = create_new_cache()


dash_app = dash.get_app()

cache = Cache(dash_app.server, config={
    'CACHE_TYPE' : 'filesystem',
    'CACHE_DIR' : '/tmp/appdash/',
    'CACHE_THRESHOLD': 100,
    'CACHE_DEFAULT_TIMEOUT': 60
})

# !!! it can delate Redis DB:
cache.clear()


#%%


from Download_And_Porcess_Data import Download_And_Process_Data


## The solution prevent to download data all times when cache is cleared, or when callbeck is fired
#ResultsDIC = Download_And_Process_Data(Authenication = 'trusted', returnData = True)

ResultsDIC = {}
ResultsDIC['HistoryTotal_1d'] = pd.read_csv('HistoryTotal_1d.csv').set_index('index')
ResultsDIC['HistoryTotal_30m'] = pd.read_csv('HistoryTotal_30m.csv').set_index('index')


@cache.memoize()
# @cache.cached()
def ReturnHistory(varName):
    

    print('jol2')
    return ResultsDIC[varName].to_json()



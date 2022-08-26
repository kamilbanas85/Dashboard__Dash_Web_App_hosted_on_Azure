import numpy as np
import pandas as pd
import datetime


import dash
from dash import dcc
from dash import html
#from dash.dependencies import Input, Output

from dash_extensions.enrich import Dash, Trigger, Output, Input, ServersideOutput, FileSystemStore

import plotly.graph_objects  as go
import plotly.express as px

# from logzero import logger
# from apscheduler.schedulers.background import BackgroundScheduler
# import atexit

import os
import pyodbc
# import feather

# pip install retry

#%%

# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)

#%%

# if os.name == 'nt':
#     FolderWithData = 'assets\\data\\'
# else:
#     FolderWithData = 'assets/data/'
    
# for f in os.listdir(FolderWithData):
#     os.remove( os.path.join(FolderWithData, f) )


#%%

from Download_And_Porcess_Data import Download_And_Process_Data


# Demand_Electricity_Texas =\
#             Download_And_Process_Data(Authenication = 'password', returnData = True)
Demand_Electricity_Texas =\
            Download_And_Process_Data(Authenication = 'trusted-azure', returnData = True)            
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'
############

# for key, val in ResultsDIC.items():
#     exec(key + '=val')


# Demand_Electricity_Texas.plot()



#%%

# Create server side store to hold the data.
fss = FileSystemStore(cache_dir="some_dir", default_timeout=10)  # timeout in seconds, i.e. yours should be 3600

LayoutRefreshTimeInMin = 5


dash_app = Dash(__name__)
app = dash_app.server

dash_app.layout = html.Div(children = [
  ######### Demand Plot
  html.Div([
    # dcc.Interval(
    #     id = 'Update_Data',
    #     interval = LayoutRefreshTimeInMin*60000,
    #     n_intervals=0),    

    #html.Div(id="log"),  # logging of data, a mock replacement of your graph
    dcc.Store(id="store_Demand"),  # store that holds the data reference
    dcc.Interval(id = "trigger",
                 interval = LayoutRefreshTimeInMin*60000),  # trigger to invoke data refresh attempt, defaults to once per second


    dcc.Graph(id='Electricity_Demand', 
              style = { 'width': '90%','display': 'inline-block' }),
    html.Div([  html.Div(children = 'Date Frequency',
                         style={'margin-top':'55px',
                                'font-weight':'bold'}),        
                dcc.RadioItems( id='Choose_frequency_demand',
                              options = [{'label':'hour', 'value':'hour'},
                                         {'label':'day', 'value':'day'},
                                         {'label':'week', 'value':'week'},                    
                                         {'label':'month', 'value':'month'}],
                              value = 'hour',
                              style={ 'margin-top': '0px' },
                              labelStyle={'display':'block'}
                              ),
            ], style={'width': '10%', 'display': 'inline-block','verticalAlign': 'top' })
    ]),
  ######### End Demand Plot

  
  
  ], style={'margin-right':'2%',
            'margin-left':'2%',
            'margin-top':'20px'})

#########################################################
#########################################################
#########################################################


TitleFontSize = 32
AxisFont = 16
AxisTitleFontSize = 16
LegendFontSize = 13


@dash_app.callback(ServersideOutput("store_Demand", "data", session_check=False, backend=fss),
                   Trigger("trigger", "n_intervals"), memoize=True)
def update_data():
    
    Demand_Electricity_Texas =\
                Download_And_Process_Data(Authenication = 'password', returnData = True)
                
    return Demand_Electricity_Texas  # put your update logic here



@dash_app.callback(
    Output('Electricity_Demand', 'figure'),
    [ Input('Choose_frequency_demand', 'value'),
      Input("store_Demand", "data")]
)
def update_figure(freqency, data):
    

    # DF = Demand_Electricity_Texas.copy()
    # if data:
    #     DF = data.copy()
    DF = data.copy()
    DF.index = pd.to_datetime(DF.reset_index()['Date'], utc = True).dt.tz_localize(None)
    
    if freqency == 'day':
        DF = DF.resample('D').mean()
    elif freqency == 'week':
        DF = DF.resample('W').mean()
    elif freqency == 'month':
        DF = DF.resample('M').mean()


    fig_Electricity_Demand = go.Figure()

    fig_Electricity_Demand.add_trace( go.Scatter(x = DF.index, y = DF.Data_01,
                                      mode = "lines" ) )
    

    Ylegend = f'Demand [Gwh/{freqency}]'
    fig_Electricity_Demand.update_layout( 
        
            template="simple_white",
            autosize=True,
            title_font_family="Times New Roman",
            
            xaxis = dict( title_text = "Date",
                          titlefont = dict(size = AxisTitleFontSize),
                          showgrid = True,
                          tickfont = dict(size = AxisFont)
                          ),
            
            yaxis = dict( title_text = Ylegend,
                          titlefont = dict(size = AxisTitleFontSize),
                          showgrid = True,
                          tickfont = dict(size = AxisFont)
                          ),   
            
            title = dict(text = "<b>Texas Electricity Demand</b>",
                         y = 1.00,
                         x = 0.5,
                         xanchor = 'center',
                         yanchor = 'top',
                         font = dict(size = TitleFontSize)
                         ),
            legend=dict(  title=None,\
                          orientation="h",\
                          y=1, 
                          yanchor="bottom", 
                          x=0.5, 
                          xanchor="center",
                          font = dict(size = LegendFontSize)
                        )
    )

    return fig_Electricity_Demand



####################################################

if __name__ == '__main__':
    
    
    dash_app.run_server(debug=True)
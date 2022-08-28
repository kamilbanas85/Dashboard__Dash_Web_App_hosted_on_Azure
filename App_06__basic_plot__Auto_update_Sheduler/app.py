import numpy as np
import pandas as pd
import datetime


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.graph_objects  as go
import plotly.express as px

import os
import pyodbc
from retry import retry

from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import feather

#%%

# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)

#%% Clear folder With Data

if os.name == 'nt': # Windows
    FolderWithData = 'asset\\Updated_Data\\'
else:
    FolderWithData = 'asset/Updated_Data/'
    

for f in os.listdir(FolderWithData):
    os.remove(os.path.join(FolderWithData, f))


#%% Download And Prcess Data

from Download_Process_And_Save_Data import Download_Process_And_Save_Data


Authenication = 'password'
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'

Download_Process_And_Save_Data(Authenication = Authenication,\
                               returnData = False,\
                               SaveData = True,\
                               FolderWithData =  FolderWithData)       


# for key, val in ResultsDIC.items():
#     exec(key + '=val')


#%% Create Plots 

LayoutRefreshTimeInMin = 5

dash_app = dash.Dash(__name__)
app = dash_app.server

dash_app.layout = html.Div(children = [
  ######### Demand Plot
  html.Div([
      
    html.Div([dcc.Interval( id = 'Update_Data',
                            interval = LayoutRefreshTimeInMin*60000,
                            n_intervals=0)]),    
    
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

@dash_app.callback(
    Output('Electricity_Demand', 'figure'),
    [ Input('Choose_frequency_demand', 'value'),
      Input('Update_Data', 'n_intervals') ]
)
def update_figure(freqency, n):
    
    
    #DF = Demand_Electricity_Texas[['Data_01']].copy()
    DF = pd.read_feather(FolderWithData+'Demand_Electricity_Texas.ftr')
    DF = DF.set_index('Date')
    
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

@app.before_first_request
def init_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    # scheduler.add_job(Download_Process_And_Save_Data, 'interval', minutes=5,\
    #                   args = [Authenication, False, True, FolderWithData])
    scheduler.add_job(Download_Process_And_Save_Data,\
                      trigger ='cron', day_of_week = 'mon-sun', hour = 14, minute = 10,\
                      args = [Authenication, False, True, FolderWithData])      

    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown(wait = False))


if __name__ == '__main__':
    
    dash_app.run_server(debug=True, use_reloader = False)


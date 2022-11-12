import dash

## add in case of multi pages !!!!!!!!!!!!!!!!!!!!!!
title = 'Home'
dash.register_page(
    __name__,
    path="/",
    title=title,
    name='Home'
)

# title, name are optional, oath ="/" only for home


import numpy as np
import pandas as pd
import datetime


from dash import Dash, dcc, html, Input, Output, callback, register_page
import dash_bootstrap_components as dbc


import plotly.graph_objects  as go
import plotly.express as px


import os
import pyodbc

from flask_caching import Cache

#%%

# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)


#%%

# from Download_And_Porcess_Data import Download_And_Process_Data


# ResultsDIC = Download_And_Process_Data(Authenication = 'trusted', returnData = True)
            
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'

#%%

# for key,val in ResultsDIC.items():
#       exec(key + '=val')


# HistoryTotal_30m
# HistoryTotal_1d

#%%

#
from Cache_data import ReturnHistory



#%%

# LayoutRefreshTimeInMin = 120


# !!! for solo page:
# dash_app = dash.Dash(__name__)
# app = dash_app.server


#  !!! for multi-page:
layout = html.Div(children = [
#  !!! for solo page:
# dash_app.layout = html.Div(children = [   
  
######### Plot
  html.Div([

    
    # dcc.Store(id="HistoryTotal_30m", data = HistoryTotal_30m.to_json() ),
    #dcc.Store(id="HistoryTotal_30m", data = HistoryTotal_30m.reset_index().to_json() ),
    # dcc.Store(id="HistoryTotal_1d", data = HistoryTotal_1d.to_json() ),
    
    html.H1('Bitcoin Price', style={'textAlign': 'center'}),

    
    html.Div(
    [
        dbc.RadioItems(
            id="History_time_select",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "   1D   ", "value": "1D"},
                {"label": "   1W   ", "value": "1W"},
                {"label": "   1M   ", "value": "1M"},
                {"label": "   1Y   ", "value": "1Y"},
                {"label": "   All  ", "value": "All"},
            ],
            value = "All",
        ),
    ],
    className="radio-group",
    ),
    
    
    html.Div([ dcc.Graph(id=f"History_All"),
               ],
                style={'margin-bottom': '60px'} ),

      
    
   ]),
  ######### End Plot

  ], style={'margin-right':'2%',
            'margin-left':'2%',
            'margin-top':'20px',
            'font-family': 'Times New Roman'})


#########################################################
#########################################################
#########################################################

def hex_to_int_color(v):
    if v[0] == '#':
        v = v[1:]
    assert(len(v) == 6)
    return int(v[:2], 16), int(v[2:4], 16), int(v[4:6], 16)

    


colorList = px.colors.qualitative.G10  



#########################################################

TitleFontSize = 32
AxisFont = 16
AxisTitleFontSize = 16
LegendFontSize = 13



#### #### DEFINE Consumption-History Plot


## In case of multi-pages !!!!!!!!!!!!!!!!!!!!!!:
# @dash_app.callback(
## In case of solo page !!!!!!!!!!!!!!!!!!!!!!:
@callback(
    Output(f"History_All", 'figure'),
    [Input("History_time_select", "value")] )
def update_Consumption_figure(Time_Selected):

    colorList = px.colors.qualitative.Dark24

    
    History_All = go.Figure()
    AxisFont = 20
    AxisTitleFontSize = 22
    LegendFontSize = 20
    TitleFontSize = 32
    
    DF = pd.DataFrame(columns = ['close','low','high'])
    
    if Time_Selected == "1D":
        DF = pd.read_json(ReturnHistory('HistoryTotal_30m')).copy()
        #HistoryTotal_30m.index[-1].date().strftime(format = '%Y-%m-%d')
        DF = DF.loc[ DF.index[-1].date().strftime(format = '%Y-%m-%d')]
    elif Time_Selected == "1W":
        DF = pd.read_json(ReturnHistory('HistoryTotal_30m')).copy()
        LastDate = DF.index[-1].date()
        DF = DF.loc[ ( LastDate- datetime.timedelta(days=7) ).strftime(format = '%Y-%m-%d') : ]    
    elif Time_Selected == "1M":
        DF = pd.read_json(ReturnHistory('HistoryTotal_30m')).copy()
        LastDate = DF.index[-1].date()
        DF = DF.loc[ ( LastDate- datetime.timedelta(days=30) ).strftime(format = '%Y-%m-%d') : ]    
    elif Time_Selected == "1Y":
        DF = pd.read_json(ReturnHistory('HistoryTotal_1d')).copy().iloc[-365:,:]
    elif Time_Selected == "All":
        DF = pd.read_json(ReturnHistory('HistoryTotal_1d')).copy()
    

        
    #DF = pd.read_json(Data_from_Store).copy()
    #DF = pd.read_json(ReturnHistory('HistoryTotal_1d'))
    #DF1 = pd.read_json(ReturnHistory('HistoryTotal_30m'))

    
    
    #Add_Forecast_Curve = False        



    # Add Plots
    var = 'Bitcoin Price'
    History_All.add_trace(go.Scatter(x=DF.index, y=DF['close'],
                         mode='lines', line={'dash': 'solid', 'color': 'red'}, legendgroup=var,  name = var)) # fill down to xaxis



    var='Price Range'
    History_All.add_trace(go.Scatter(x=DF.index, y=DF['low'],
                       marker_color = 'rgba(0,0,0,0.0)', showlegend = False, name = var)) # fill down to xaxis
    History_All.add_trace(go.Scatter(x=DF.index, y=DF['high'],
                       name = var,  legendgroup=var, fill='tonexty',  mode= 'none', fillcolor = 'rgba(0,0,255,0.3)')) # fill down to xaxis   



    Ylegend = f'USD'
    History_All.update_layout( 
        
            template="simple_white",
            autosize=True,
            font_family="Times New Roman",
            title_font_family="Times New Roman",
            
            xaxis = dict( title_text = "Time UTC",
                          titlefont = dict(size = AxisTitleFontSize),
                          showgrid = True,
                          tickfont = dict(size = AxisFont)
                          ),
            
            yaxis = dict( title_text = Ylegend,
                          titlefont = dict(size = AxisTitleFontSize),
                          showgrid = True,
                          tickfont = dict(size = AxisFont),),   

            # title = dict(text = "<b>Bitcoin Price</b>",
            #              y = 1.00,
            #              x = 0.5,
            #              xanchor = 'center',
            #              yanchor = 'top',
            #              font = dict(size = TitleFontSize)
            #              ),
            legend=dict(  title=None,\
                          orientation="h",\
                          y=1, 
                          yanchor="bottom", 
                          x=0.5, 
                          xanchor="center",
                          font = dict(size = LegendFontSize)
                        ),
            margin=dict(t=0)
    ),
        
        
        
    
    return History_All





# for solo pages:
# if __name__ == '__main__':
    
#     dash_app.run_server(debug=True)
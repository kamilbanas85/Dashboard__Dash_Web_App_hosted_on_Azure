import dash

## add in case of multi pages !!!!!!!!!!!!!!!!!!!!!!
title = 'Volatillity'
dash.register_page(
    __name__,
    #path="/",
    title=title,
    name='Volatillity'
)

# title, name are optional, oath ="/" only for home


import numpy as np
import pandas as pd
import datetime


from dash import Dash, dcc, html, Input, Output, callback, register_page

import plotly.graph_objects  as go
import plotly.express as px


import os
import pyodbc


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

from Cache_data import ReturnHistory


########################################################
#%% Read Data From Disk

def CreateMarks( DF ):
    
    MarksAll = {i:datetime.datetime.strftime(x, "%d-%m-%Y") for i,x in enumerate(DF.index.to_list())}
    MarksMax = len(MarksAll) -1
    
    Marks = {key:value[-4:] for key, value in MarksAll.items() if datetime.datetime.strptime(value, "%d-%m-%Y").month == 1 and 
                                                                  datetime.datetime.strptime(value, "%d-%m-%Y").day == 1}
    try:
        Marks[0]
    except:
        Marks[0] = ''  
    
    
    try:
        Marks[MarksMax]
    except:
        Marks[MarksMax] = ''
    
    return Marks


def CreteStartAndMaxMarks(MarksDic):
    
    MarksStartValue = list({key:value for key, value in MarksDic.items() if value == str(datetime.datetime.now().year - 3)}.keys())[0]
    MarksMax = max( list(MarksDic.keys() ) )
    
    return MarksStartValue, MarksMax


HistoryTotal_1d = pd.read_json(ReturnHistory('HistoryTotal_1d'))
Hist_Marks = CreateMarks(HistoryTotal_1d)

Hist_MarksStartValue, Hist_MarksMax = CreteStartAndMaxMarks(Hist_Marks)

#%%


# !!! for solo page:
# dash_app = dash.Dash(__name__)
# app = dash_app.server


#  !!! for multi-page:
layout = html.Div(children = [

#  !!! for solo page:
# dash_app.layout = html.Div(children = [   
  ######### Demand Plot
  html.Div([

    
    # dcc.Store(id="HistoryTotal_30m", data = HistoryTotal_30m.to_json() ),
    #dcc.Store(id="HistoryTotal_30m", data = HistoryTotal_30m.reset_index().to_json() ),
    # dcc.Store(id="HistoryTotal_1d", data = HistoryTotal_1d.to_json() ),
    
    html.Div([ dcc.Graph(id=f"History_1d"),
               dcc.RangeSlider( id=f"Slider_History_1d",
                                   marks = Hist_Marks,
                                   min = 0,
                                   max = Hist_MarksMax,
                                   value = [ Hist_MarksStartValue, Hist_MarksMax ]
                      )
                ],
                style={'margin-bottom': '60px'} ),

    html.Div([ dcc.Graph(id=f"Return_1d"),
               dcc.RangeSlider( id=f"Slider_Return_1d",
                                   marks = Hist_Marks,
                                   min = 0,
                                   max = Hist_MarksMax,
                                   value = [ Hist_MarksStartValue, Hist_MarksMax ]
                      )
                ],
                style={'margin-bottom': '60px'} ),
      
    
   ]),
  ######### End Demand Plot

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

## In case of solo page !!!!!!!!!!!!!!!!!!!!!!:
@callback(
## In case of multi-pages !!!!!!!!!!!!!!!!!!!!!!:
# @dash_app.callback(
    Output(f"History_1d", 'figure'),
    [Input(f"Slider_History_1d", 'value')] )
def update_Consumption_figure(Slider):

    
    colorList = px.colors.qualitative.Dark24

    
    figHist_1d = go.Figure()
    AxisFont = 16
    AxisTitleFont = 16
    LegendFontSize = 16
    TitleFontSize = 32
    
        
        
    #DF = pd.read_json(Data_from_Store).copy()
    DF = pd.read_json(ReturnHistory('HistoryTotal_1d'))
  
    if Slider[1] == DF.shape[0]-1:
        DF = DF.iloc[ Slider[0] : Slider[1]+1 ]
    else:
        DF = DF.iloc[ Slider[0] : Slider[1] ]


    # Add Plots
    var = 'Bitcoin Price'
    figHist_1d.add_trace(go.Scatter(x=DF.index, y=DF['close'],
                         mode='lines', line={'dash': 'solid', 'color': 'red'}, legendgroup=var,  name = var)) # fill down to xaxis



    var='Price Range'
    figHist_1d.add_trace(go.Scatter(x=DF.index, y=DF['low'],
                       marker_color = 'rgba(0,0,0,0.0)', showlegend = False, name = var)) # fill down to xaxis
    figHist_1d.add_trace(go.Scatter(x=DF.index, y=DF['high'],
                       name = var,  legendgroup=var, fill='tonexty',  mode= 'none', fillcolor = 'rgba(0,0,255,0.3)')) # fill down to xaxis   



    Ylegend = f'USD'
    figHist_1d.update_layout( 
        
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
            
            title = dict(text = "<b>Bitcoin Price</b>",
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

    return figHist_1d


##################################################################################
#### #### DEFINE Return-History Plot

## In case of solo page !!!!!!!!!!!!!!!!!!!!!!:
@callback(
## In case of multi-pages !!!!!!!!!!!!!!!!!!!!!!:
# @dash_app.callback(
    Output(f"Return_1d", 'figure'),
    [Input(f"Slider_Return_1d", 'value')] )
def update_Consumption_figure(Slider):

    
    colorList = px.colors.qualitative.Dark24

    
    figReturn_1d = go.Figure()
    AxisFont = 16
    AxisTitleFont = 16
    LegendFontSize = 16
    TitleFontSize = 32
    
        
        
    #DF = pd.read_json(Data_from_Store).copy()
    DF = pd.read_json(ReturnHistory('HistoryTotal_1d'))

    if Slider[1] == DF.shape[0]-1:
        DF = DF.iloc[ Slider[0] : Slider[1]+1 ]
    else:
        DF = DF.iloc[ Slider[0] : Slider[1] ]


    # Add Plots
    var = 'Return Bitcoin Price'
    figReturn_1d.add_trace(go.Scatter(x=DF.index, y=DF['Return'],
                         mode='lines', line={'dash': 'solid', 'color': 'red'}, legendgroup=var,  name = var)) # fill down to xaxis


    Ylegend = f'%'
    figReturn_1d.update_layout( 
        
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
            
            title = dict(text = "<b>Return - Bitcoin Price</b>",
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

    return figReturn_1d




# for solo page:
# if __name__ == '__main__':
    
#     dash_app.run_server(debug=True)
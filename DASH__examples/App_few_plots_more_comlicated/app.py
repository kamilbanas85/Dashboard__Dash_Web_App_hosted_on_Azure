import numpy as np
import pandas as pd
import datetime


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.graph_objects  as go
import plotly.express as px

from logzero import logger
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import os
import pyodbc
# import feather

# pip install retry

#%%

MainDirectory = os.path.abspath(os.path.dirname(__file__))
os.chdir(MainDirectory)

#%%

# if os.name == 'nt':
#     FolderWithData = 'assets\\data\\'
# else:
#     FolderWithData = 'assets/data/'
    
# for f in os.listdir(FolderWithData):
#     os.remove( os.path.join(FolderWithData, f) )


#%%

# from Download_And_Porcess_Data import Download_And_Process_Data


# Demand_Electricity_Texas, Demand_Electricity_TexasForecast =\
#             Download_And_Process_Data(Authenication = 'password', returnData = True)
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'
############

# for key, val in ResultsDIC.items():
#     exec(key + '=val')


# Demand_Electricity_Texas.plot()
# Demand_Electricity_Texas.to_csv('Demand_Electricity_Texas.csv')
# Demand_Electricity_TexasForecast.to_csv('Demand_Electricity_TexasForecast.csv')

Demand_Electricity_Texas = pd.read_csv('Demand_Electricity_Texas.csv')\
                                .assign(Date = lambda x: pd.to_datetime(x['Date']))\
                                .set_index('Date')
                                
Demand_Electricity_TexasForecast = pd.read_csv('Demand_Electricity_TexasForecast.csv').rename(columns = {'Unnamed: 0':'Date'})\
                                       .assign(Date = lambda x: pd.to_datetime(x['Date']))\
                                       .set_index('Date')


#%%

# LayoutRefreshTimeInMin = 120

dash_app = dash.Dash(__name__)
app = dash_app.server

dash_app.layout = html.Div(children = [
  ######### Demand Plot
  html.Div([
    # html.Div([dcc.Interval(
    #     id = 'Update_Data',
    #     interval = LayoutRefreshTimeInMin*60000,
    #     n_intervals=0),    
    
    
    # Basic Plot - change frequency of date
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
  
  ######### Start Plot - Add forecast for 2 curves 
  html.Div([
  
    
    dcc.Graph(id='Electricity_Demand_02', 
              style = { 'width': '90%','display': 'inline-block' }),
    html.Div([  html.Div(children = 'Date Range',
                       style={'margin-top':'55px',
                              'font-weight':'bold'}),        
                dcc.RadioItems( id='Demand__Forecast',
                            options = [{'label':'History', 'value':'History'},
                                       {'label':'Add Forecast', 'value':'Add_Forecast'}],
                            value = 'History',
                            style={ 'margin-top': '0px' },
                            labelStyle={'display':'block'}
                            ),
        
                html.Div(children = 'Date Frequency',
                         style={'margin-top':'15px',
                                'font-weight':'bold'}),        
                dcc.RadioItems( id='Choose_frequency_demand_02',
                              options = [{'label':'hour', 'value':'hour'},
                                         {'label':'day', 'value':'day'},
                                         {'label':'week', 'value':'week'},                    
                                         {'label':'month', 'value':'month'}],
                              value = 'hour',
                              style={ 'margin-top': '0px' },
                              labelStyle={'display':'block'}
                              )                
                
            ], style={'width': '10%', 'display': 'inline-block','verticalAlign': 'top' })
    ]),
  
  ######### Start 3 plot - range between f.e. min - max from few years etc. and its forecast
  
  html.Div([
    
    dcc.Graph(id='Electricity_Demand_03', 
              style = { 'width': '90%','display': 'inline-block' }),
    html.Div([  html.Div(children = 'Date Range',
                       style={'margin-top':'55px',
                              'font-weight':'bold'}),        
                dcc.RadioItems( id='Add__Forecast_03',
                            options = [{'label':'History', 'value':'History'},
                                       {'label':'Add Forecast', 'value':'Add_Forecast'}],
                            value = 'History',
                            style={ 'margin-top': '0px' },
                            labelStyle={'display':'block'}
                            ),
                     
                
            ], style={'width': '10%', 'display': 'inline-block','verticalAlign': 'top' })
    ]),
  
  ######### Start 4 plot - button depend on other button state
  
  html.Div([
    
    dcc.Graph(id='Electricity_Demand_04', 
              style = { 'width': '90%','display': 'inline-block' }),
    html.Div([   html.Div(children = 'Date Frequency',
                             style={'margin-top':'15px',
                                    'font-weight':'bold'}),        
                 dcc.RadioItems( id='Choose_frequency_demand_04',
                                  options = [{'label':'day', 'value':'day'},
                                             {'label':'week', 'value':'week'}],
                                  value = 'day',
                                  style={ 'margin-top': '0px' },
                                  labelStyle={'display':'block'}
                                  ),     
        
        
                 html.Div( [ html.Div(children = 'Date Range',
                                      style={'margin-top':'55px',
                                             'font-weight':'bold'}),        
                             dcc.RadioItems( id='Add__Forecast_04',
                                           options = [{'label':'History', 'value':'History'},
                                                      {'label':'Add Forecast', 'value':'Add_Forecast'}],
                                           value = 'History',
                                           style={ 'margin-top': '0px' },
                                           labelStyle={'display':'block'} ),
                           ],
                           id='Date Range visibility' ),
                     
                
            ], style={'width': '10%', 'display': 'inline-block','verticalAlign': 'top' })
    ])    
  
  
  ], style={'margin-right':'2%',
            'margin-left':'2%',
            'margin-top':'20px'})

#########################################################
#########################################################
#########################################################

def hex_to_int_color(v):
    if v[0] == '#':
        v = v[1:]
    assert(len(v) == 6)
    return int(v[:2], 16), int(v[2:4], 16), int(v[4:6], 16)

    


def AddLinearPlot(DF, Vars, colors, fig, DFforcast = None, Add_Forecast = True):    
     
    for i, var in enumerate( Vars ):
        colorRGB = hex_to_int_color(colors[i])
        colorRGBstr = 'rgb'+str(colorRGB)
        
        DFcurrent = DF.copy()[[var]].dropna()
        fig.add_trace(go.Scatter(x=DFcurrent.index, y=DFcurrent[var],  stackgroup="one", mode='none', fillcolor = colorRGBstr,  name = var,  legendgroup=var)) # fill down to xaxis
        if Add_Forecast:
            DFforcastcurrent = DFforcast.copy().filter(regex = var).dropna()            
            colorRGBAstr = 'rgba'+str((*colorRGB,0.5))
            fig.add_trace(go.Scatter(x=DFforcastcurrent.index, y=DFforcastcurrent.iloc[:,0],
                                     stackgroup="one", mode='none', fillcolor = colorRGBAstr,  name = DFforcastcurrent.iloc[:,0].name, legendgroup=var)) # fill down to xaxis


def AddBarPlot(DF, Vars, colors, fig,  DFforcast = None, Add_Forecast = True):    
     
    for i, var in enumerate( Vars ):
        colorRGB = hex_to_int_color(colors[i])
        colorRGBstr = 'rgb'+str(colorRGB)
        
        DFcurrent = DF.copy()[[var]].dropna()
        fig.add_trace(go.Bar(x=DFcurrent.index, y=DFcurrent[var],  name = var,  legendgroup=var, marker_color = colorRGBstr)) # fill down to xaxis
        if Add_Forecast:
            DFforcastcurrent = DFforcast.copy().filter(regex = var).dropna()
            colorRGBAstr = 'rgba'+str((*colorRGB,0.5))
            fig.add_trace(go.Bar(x=DFforcastcurrent.index, y=DFforcastcurrent.iloc[:,0], 
                                 name = DFforcastcurrent.iloc[:,0].name, legendgroup=var, marker_color = colorRGBAstr)) # fill down to xaxis



colorList = px.colors.qualitative.G10  



#########################################################
### PLOT 1

TitleFontSize = 32
AxisFont = 16
AxisTitleFontSize = 16
LegendFontSize = 13

@dash_app.callback(
    Output('Electricity_Demand', 'figure'),
    [ Input('Choose_frequency_demand', 'value') ]
)
def update_figure(freqency):
    
    
    DF = Demand_Electricity_Texas[['Data_01']].copy()
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



##################################################################
### Plot 2

@dash_app.callback(
    Output('Electricity_Demand_02', 'figure'),
    [ Input('Choose_frequency_demand_02', 'value'),
     Input( 'Demand__Forecast', 'value')]
)
def update_figure(freqency, Add_or_No_Forecast_Curve):
    
    
    DF = Demand_Electricity_Texas.copy()
    DFforecast = Demand_Electricity_TexasForecast.copy()
        
    
    LegendFontSize = 13
    if Add_or_No_Forecast_Curve == 'Add_Forecast':
        Add_Forecast_Curve = True
        LegendFontSize = 10

    else:
        Add_Forecast_Curve = False        
    
    scalerUnit = 1       
    VarList = list( DF.columns )
    
    fig_Electricity_Demand_02 = go.Figure()
   
    # Add Plots
    if freqency == "hour":
        AddLinearPlot(DF = (DF*scalerUnit).dropna(how = 'all'), Vars = VarList, colors = colorList, fig = fig_Electricity_Demand_02,
                      DFforcast = (DFforecast*scalerUnit).dropna(how = 'all'), Add_Forecast = Add_Forecast_Curve)
    elif  freqency == "day":
        AddLinearPlot(DF = (DF*scalerUnit).dropna(how = 'all').resample('D').sum(), Vars = VarList, colors = colorList, fig = fig_Electricity_Demand_02,
                      DFforcast = (DFforecast*scalerUnit).dropna(how = 'all').resample('D').sum(), Add_Forecast = Add_Forecast_Curve)
    elif  freqency == "week":
        AddBarPlot(DF = (DF*scalerUnit).dropna(how = 'all').resample("w-mon").sum(), Vars = VarList, colors = colorList, fig = fig_Electricity_Demand_02,
                   DFforcast = (DFforecast*scalerUnit).dropna(how = 'all').resample("w-mon").sum(), Add_Forecast = Add_Forecast_Curve)
    elif  freqency == "month":
        AddBarPlot(DF = (DF*scalerUnit).dropna(how = 'all').resample("MS").sum(), Vars = VarList, colors = colorList, fig = fig_Electricity_Demand_02,
                   DFforcast = (DFforecast*scalerUnit).dropna(how = 'all').resample("MS").sum(), Add_Forecast = Add_Forecast_Curve)
   



    Ylegend = f'Demand [Gwh/{freqency}]'
    
    fig_Electricity_Demand_02.update_layout( 
        
            template="simple_white",
            autosize=True,
            title_font_family="Times New Roman",
            
            barmode='stack',
            
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
                          x=0.17, 
                          xanchor="center",
                          font = dict(size = LegendFontSize)
                        )
    )
        
    
    
    return fig_Electricity_Demand_02

##################################################################
### PLOT 3

@dash_app.callback(
    Output('Electricity_Demand_03', 'figure'),
    [ Input( 'Add__Forecast_03', 'value')]
)
def update_figure(Add_or_No_Forecast_Curve):
    
    #### Prepare Data
    DF = Demand_Electricity_Texas[['Data_01']].copy()
    DFforecast = Demand_Electricity_TexasForecast[['Data_01__Forecast']].copy()
    
    DF = DF.dropna(how = 'all').resample('D').mean()
    DFforecast = DFforecast.dropna(how = 'all').resample('D').mean()
    
    DF['Month-Day'] = DF.index.strftime('%m-%d')
    DFforecast['Month-Day'] = DFforecast.index.strftime('%m-%d')

    AVG = DF.groupby(['Month-Day'] ).mean().rename(columns = {'Data_01':'avg'})
    AVG['top'] = DF.groupby( ['Month-Day'] )['Data_01'].max()
    AVG['bottom'] = DF.groupby( ['Month-Day']  )['Data_01'].min()
    
    
    AVGforecast = DFforecast.groupby(['Month-Day'] ).mean().rename(columns = {'Data_01__Forecast':'avg__Forecast'})
    AVGforecast['top__forecast'] = DFforecast.groupby( ['Month-Day'] )['Data_01__Forecast'].max() + 5000
    AVGforecast['bottom__forecast'] = DFforecast.groupby( ['Month-Day'] )['Data_01__Forecast'].min() - 5000
    
    #####
    
    
    DF = DF.reset_index()\
        .merge(AVG, how= 'left',  left_on = 'Month-Day', right_on = 'Month-Day')\
        .set_index('Date')
        
    DFforecast = DFforecast.reset_index()\
        .merge(AVGforecast, how= 'left',  left_on = 'Month-Day', right_on = 'Month-Day')\
        .set_index('Date')    
    
                     
     
    
    LegendFontSize = 13
    if Add_or_No_Forecast_Curve == 'Add_Forecast':
        Add_Forecast_Curve = True
        LegendFontSize = 10

    else:
        Add_Forecast_Curve = False        
    
    scalerUnit = 1       
    VarList = list( DF.columns )
    
    fig_Electricity_Demand_03 = go.Figure()
   
    # Add Plots
    var = 'Data_01'
    fig_Electricity_Demand_03.add_trace(go.Scatter(x=DF.index, y=DF['Data_01'],
                         mode='lines', line={'dash': 'solid', 'color': 'red'}, legendgroup=var,  name = 'Data 01')) # fill down to xaxis
    if Add_or_No_Forecast_Curve == 'Add_Forecast':
         fig_Electricity_Demand_03.add_trace(go.Scatter(x=DFforecast.index, y=DFforecast['Data_01__Forecast'],
                          mode='lines', line={'dash': 'dash', 'color': 'red'}, name = 'Data 01 - Forecast',  legendgroup=var)) # fill down to xaxis

    var = 'avg'
    fig_Electricity_Demand_03.add_trace(go.Scatter(x=DF.index, y=DF['avg'],\
                 mode='lines', line={'dash': 'solid', 'color': 'blue'}, legendgroup=var,  name = 'avg')) # fill down to xaxis
    if Add_or_No_Forecast_Curve == 'Add_Forecast':
         fig_Electricity_Demand_03.add_trace(go.Scatter(x=DFforecast.index, y=DFforecast['avg__Forecast'],
                          mode='lines', line={'dash': 'dash', 'color': 'blue'}, name = 'avg - forecast',  legendgroup=var)) # fill down to xaxis
    

    var='Range'
    fig_Electricity_Demand_03.add_trace(go.Scatter(x=DF.index, y=DF['bottom'],
                       marker_color = 'rgba(0,0,0,0.0)', showlegend = False, name = var)) # fill down to xaxis
    fig_Electricity_Demand_03.add_trace(go.Scatter(x=DF.index, y=DF['top'],
                       name = var,  legendgroup=var, fill='tonexty',  mode= 'none', fillcolor = 'rgba(0,0,255,0.3)')) # fill down to xaxis                         
    if Add_or_No_Forecast_Curve == 'Add_Forecast':
        fig_Electricity_Demand_03.add_trace(go.Scatter(x=DFforecast.index, y=DFforecast['bottom__forecast'],
                        marker_color = 'rgba(0,0,0,0.0)', showlegend = False,
                        name = 'Range Forecast')) # fill down to xaxis
        fig_Electricity_Demand_03.add_trace(go.Scatter(x=DFforecast.index, y=DFforecast['top__forecast'],
                         name = 'Range Forecast',  legendgroup=var, fill='tonexty', mode= 'none', fillcolor = 'rgba(0,0,255,0.1)')) # fill down to xaxis 
     

    Ylegend = f'Demand [Gwh/day]'
    
    fig_Electricity_Demand_03.update_layout( 
        
            template="simple_white",
            autosize=True,
            title_font_family="Times New Roman",
            
            barmode='stack',
            
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
                          x=0.17, 
                          xanchor="center",
                          font = dict(size = LegendFontSize)
                        )
    )
        
    
    
    return fig_Electricity_Demand_03


##################################################################
### PLOT 4

@dash_app.callback(
    Output(component_id='Date Range visibility', component_property='style'),
   [Input(component_id='Choose_frequency_demand_04', component_property='value')])

def show_hide_element(visibility_state):
    if visibility_state == 'week':
        return {'display': 'block'}
    if visibility_state == 'day':
        return {'display': 'none'}



@dash_app.callback(
    Output('Electricity_Demand_04', 'figure'),
    [ Input('Choose_frequency_demand_04', 'value'),
     Input( 'Add__Forecast_04', 'value')]
)
def update_figure(freqency, Add_or_No_Forecast_Curve):
    
    
    DF = Demand_Electricity_Texas.copy()
    DFforecast = Demand_Electricity_TexasForecast.copy()
        
    
    LegendFontSize = 13
    if Add_or_No_Forecast_Curve == 'Add_Forecast':
        Add_Forecast_Curve = True
        LegendFontSize = 10

    else:
        Add_Forecast_Curve = False        
    
    scalerUnit = 1       
    VarList = list( DF.columns )
    
    fig_Electricity_Demand_04 = go.Figure()
   
    # Add Plots
    if  freqency == "day":
        AddLinearPlot(DF = (DF*scalerUnit).dropna(how = 'all').resample('D').sum(), Vars = VarList, colors = colorList, fig = fig_Electricity_Demand_04,
                      DFforcast = (DFforecast*scalerUnit).dropna(how = 'all').resample('D').sum(), Add_Forecast = Add_Forecast_Curve)
    elif  freqency == "week":
        AddBarPlot(DF = (DF*scalerUnit).dropna(how = 'all').resample("w-mon").sum(), Vars = VarList, colors = colorList, fig = fig_Electricity_Demand_04,
                   DFforcast = (DFforecast*scalerUnit).dropna(how = 'all').resample("w-mon").sum(), Add_Forecast = Add_Forecast_Curve)



    Ylegend = f'Demand [Gwh/{freqency}]'
    
    fig_Electricity_Demand_04.update_layout( 
        
            template="simple_white",
            autosize=True,
            title_font_family="Times New Roman",
            
            barmode='stack',
            
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
                          x=0.17, 
                          xanchor="center",
                          font = dict(size = LegendFontSize)
                        )
    )
        
    
    
    return fig_Electricity_Demand_04


####################################################################


if __name__ == '__main__':
    
    
    dash_app.run_server(debug=True)
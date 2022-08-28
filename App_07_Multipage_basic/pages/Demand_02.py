import dash

dash.register_page(__name__)


import numpy as np
import pandas as pd
import datetime


from dash import Dash, dcc, html, Input, Output, callback, register_page

import plotly.graph_objects  as go
import plotly.express as px

import os
import pyodbc


#%%


layout = html.Div(children = [
  ######### Demand Plot


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

TitleFontSize = 32
AxisFont = 16
AxisTitleFontSize = 16
LegendFontSize = 13



@callback(
    Output('Electricity_Demand_02', 'figure'),
    [ Input('Choose_frequency_demand_02', 'value'),
      Input( 'Demand__Forecast', 'value'),
      Input("store_Demand_01", "data"),
      Input("store_Demand_02", "data")]
)
def update_figure(freqency, Add_or_No_Forecast_Curve, df, df_Forecast):
    
    
    # DF = Demand_Electricity_Texas.copy()
    # DFforecast = Demand_Electricity_TexasForecast.copy()
    DF = pd.read_json(df).copy()
    DFforecast = pd.read_json(df_Forecast).copy()
        
    
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




# if __name__ == '__main__':
    
    
#     dash_app.run_server(debug=True)
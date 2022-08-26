import dash

dash.register_page(__name__, path='/')


import numpy as np
import pandas as pd
import datetime


from dash import Dash, dcc, html, Input, Output, callback, register_page


import plotly.graph_objects  as go
import plotly.express as px


import os
import pyodbc
# import feather

# pip install retry

#%%

# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)


#%%

# from Download_And_Porcess_Data import Download_And_Process_Data


# Demand_Electricity_Texas, Demand_Electricity_TexasForecast =\
#             Download_And_Process_Data(Authenication = 'password', returnData = True)
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'



#%%

# LayoutRefreshTimeInMin = 120

# dash_app = dash.Dash(__name__)
# app = dash_app.server



layout = html.Div(children = [
  ######### Demand Plot
  html.Div([
    # html.Div([dcc.Interval(
    #     id = 'Update_Data',
    #     interval = LayoutRefreshTimeInMin*60000,
    #     n_intervals=0),    
    
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
    Output('Electricity_Demand', 'figure'),
    [ Input('Choose_frequency_demand', 'value'),
      Input("store_Demand_01", "data")]
)
def update_figure(freqency, df):
    
    DF = pd.read_json(df).copy()[['Data_01']].copy()
 #   DF = Demand_Electricity_Texas[['Data_01']].copy()
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



# if __name__ == '__main__':
    
    
#     dash_app.run_server(debug=True)
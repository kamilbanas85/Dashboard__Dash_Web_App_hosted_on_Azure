import os 
import pyodbc as pyodbc
import pandas as pd
import numpy as np

import datetime

import statsmodels.api as sm
import statsmodels.formula.api as smf

import plotly.graph_objects as go
import plotly.express as px


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

#%%

MainDirectory = os.path.abspath(os.path.dirname(__file__))
os.chdir(MainDirectory)


#%% Import Data and Prepare data

Demand_Electricity_Texas = pd.read_csv('Demand_Electricity_Texas.csv')\
                                .assign(Date = lambda x: pd.to_datetime(x['Date']))\
                                .set_index('Date')[['Data_01']]
   


Demand_Electricity_Texas_Daily =  Demand_Electricity_Texas.resample('D').sum()




#################################################
#%% PRAPARE DATA PER GAS YEAR

from Prepare_Data_Per_Year import prepare_data_perYear, prepare_data_perGasYear
varMain = 'Data_01'


NumberOfYearsToInclude = 1
DICperGasYear = prepare_data_perGasYear(Demand_Electricity_Texas_Daily, NumberOfYearsToInclude)
DICperYear = prepare_data_perYear(Demand_Electricity_Texas_Daily, NumberOfYearsToInclude)



########################################################
#%% ###########################################

#%% CREATE LAYOUT

dash_app = dash.Dash(__name__)
app = dash_app.server

dash_app.layout = html.Div(children = [
   
#    html.H1(children = 'Natural Gas Consumption in Europe',
#                        style={'text-align': 'center'}),
    html.Div([ dcc.Graph(id='Compare_Years-plot',
                         style={'width': '85%',  'display': 'inline-block'}),
               html.Div([  html.Div(children = 'Plot Type',
                                    style={"margin-top": "55px", 
                                           "font-weight": "bold"}),

                           dcc.RadioItems( id='Plot_Type',
                                        options=[ {'label': 'History', 'value': 'History'},
                                                  {'label': 'Compare Gas Year', 'value': 'Compare_Gas_Year'},
                                                  {'label': 'Compare Years', 'value': 'Compare_Year'}                                       
                                                ],
                                        value = "History",
                                        style={"margin-top": "0px"},
                                        labelStyle={'display': 'block'}), 
                           
                          html.Div( [html.Div(children = 'Select Variable',
                                    style={"margin-top": "15px", 
                                           "font-weight": "bold"}),                   
                                    dcc.Dropdown( id='Variable_Selected',
                                        options=[{'label': VarName, 'value': VarName} for VarName in DICperYear.keys()],
                                        value = list(DICperYear.keys())[0],
                                        style={"margin-top": "0px"})
                                   ], 
                                   id='Slected_variable' ),                          


                        ],
                        style={'width': '15%',  'display': 'inline-block', 'vertical-align': 'top'} )
               
             ], style = {'margin-bottom': '60px'})
    ])





########################################################
#%%  MAKE PLOT


# Hide element for Compare Years
@dash_app.callback(
    Output(component_id='Slected_variable', component_property='style'),    
   [Input(component_id='Plot_Type', component_property='value')])
def show_hide_element(visibility_state):
    if visibility_state == 'History':
        return {'display': 'none'}
    else:
        return {'display': 'block'}
    

@dash_app.callback(
    Output('Compare_Years-plot', 'figure'),
    [Input('Plot_Type', 'value'),
     Input('Variable_Selected', 'value')])
def update_CompareYear_figure(Plot_Type, VariableSelected):

    
    
    #####
    
    figComapreYear = go.Figure()
    
    colorList = px.colors.qualitative.G10
    #colorList = px.colors.qualitative.D3
    
    tickformatAGSI = None
    dtickAGSI = None
    
    
    if Plot_Type == 'History':
        
            BasicDF = Demand_Electricity_Texas_Daily.copy()
            VarName = 'Data_01'
            
            figComapreYear.add_trace(go.Scatter(x=BasicDF.index, y=BasicDF[VarName],
                             mode='lines', line={ 'color': colorList[0]}, name = VarName,  legendgroup=VarName)) # fill down to xaxis

        
    elif Plot_Type == 'Compare_Gas_Year' or 'Compare_Year':
    
        
        # DFagsiCountryPerGasYear.columns
        IndexDateListPerGasYear = pd.date_range(datetime.datetime(2020, 10, 1).strftime('%Y-%m-%d'), periods=365).tolist()   
        IndexDateListPerYear = pd.date_range(datetime.datetime(2020, 1, 1).strftime('%Y-%m-%d'), periods=365).tolist()          
        # !!!! Choose Plot Type
        if Plot_Type == 'Compare_Gas_Year':
            DFgasYears = DICperGasYear[ VariableSelected ].copy()
            IndexDateList = IndexDateListPerGasYear

        elif Plot_Type == 'Compare_Year':
            DFgasYears = DICperYear[ VariableSelected ].copy()
            IndexDateList = IndexDateListPerYear

        
        
        for gasYear in DFgasYears.columns[:(NumberOfYearsToInclude+1)]:
            figComapreYear.add_trace(go.Scatter(x=IndexDateList , y=DFgasYears[gasYear], mode='lines' , name = gasYear))
                
        var='5 Years Avg'
        figComapreYear.add_trace(go.Scatter(x=IndexDateList, y=DFgasYears['avg_5years'], mode='lines',
                                  line={'dash': 'solid', 'color': 'blue'}, name = var)) # fill down to xaxis
        
        var='5 Years Range'
        figComapreYear.add_trace(go.Scatter(x=IndexDateList, y=DFgasYears['min_5years'],
                                  marker_color = 'rgba(0,0,0,0.0)', showlegend = False, name = var)) # fill down to xaxis
        figComapreYear.add_trace(go.Scatter(x=IndexDateList, y=DFgasYears['max_5years'],
                                  name = var,  legendgroup=var, fill='tonexty',  mode= 'none', fillcolor = 'rgba(192,192,192, 0.5)')) # fill down to xaxis                         
        
        
        
        tickformatAGSI = '%b-%d'
        dtickAGSI = 'M1'
            
    
    AxisFont = 18
    AxisTitleFont = 20
    LegendFontSize = 20
    TitleFontSize = 26 
    
    
    figComapreYear.update_layout(
                    template="simple_white",
                    autosize=True,
                    title_font_family="Times New Roman",
      
                    legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            font = dict(size=LegendFontSize)
                            ),  
    
                    xaxis=dict(
                            title_text="Date",
                            titlefont = dict(size = AxisTitleFont),
                            showgrid = True,
    #                        tickvals = pd.DataFrame(index = datelist).index.strftime('%b'),
                            tickformat = tickformatAGSI,
                            dtick = dtickAGSI,
                            tickfont = dict(size=AxisFont)
                            ),
      
                    yaxis=dict(
                            title ="Value [ GWh/day ]",
                            titlefont = dict(size = AxisTitleFont),
                            showgrid = True,
                            tickfont = dict(size=AxisFont)
                            ),
      
                   title=dict( text = "<b>Gas Consumption</b>",
                            y = 1.00,
                            x = 0.5,
                            xanchor = 'center',
                            yanchor = 'top',
                            font = dict(size=TitleFontSize)
                            )
    )
    
    
    return figComapreYear
    
##########################################################  
    
if __name__ == '__main__':
    dash_app.run_server(debug=True)
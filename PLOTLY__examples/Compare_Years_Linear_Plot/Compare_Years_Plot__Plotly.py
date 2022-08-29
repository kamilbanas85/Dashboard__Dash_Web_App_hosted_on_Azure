import os 
import pyodbc as pyodbc
import pandas as pd
import numpy as np

import datetime

import statsmodels.api as sm
import statsmodels.formula.api as smf

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio



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

DFperGasYear = DICperGasYear[ varMain ]
DFperYear = DICperYear[ varMain ]

########################################################
#%%  MAKE PLOT

### Import to open in browser
pio.renderers.default='browser'

#####

figComapreYear = go.Figure()

colorList = px.colors.qualitative.G10
#colorList = px.colors.qualitative.D3

tickformatAGSI = None
dtickAGSI = None
    
# DFagsiCountryPerGasYear.columns
IndexDateListPerGasYear = pd.date_range(datetime.datetime(2020, 10, 1).strftime('%Y-%m-%d'), periods=365).tolist()   
IndexDateListPerYear = pd.date_range(datetime.datetime(2020, 1, 1).strftime('%Y-%m-%d'), periods=365).tolist()          
# !!!! Choose Plot Type
IndexDateList = IndexDateListPerYear
DF = DFperYear
#!!!!!


DFgasYears = DF.copy()


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
AxisTitleFont = 22
LegendFontSize = 22
TitleFontSize = 30  


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


figComapreYear.show()

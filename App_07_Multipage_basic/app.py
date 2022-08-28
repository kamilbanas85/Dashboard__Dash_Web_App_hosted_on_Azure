import dash
import dash_bootstrap_components as dbc

import numpy as np
import pandas as pd
import datetime

from dash import Dash, dcc, html, Input, Output, callback

import plotly.graph_objects  as go
import plotly.express as px

import os
import pyodbc
# import feather


#%%

# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)

#%%

from Download_And_Porcess_Data import Download_And_Process_Data


Demand_Electricity_Texas, Demand_Electricity_TexasForecast =\
            Download_And_Process_Data(Authenication = 'password', returnData = True)
            
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'

#%%

# LayoutRefreshTimeInMin = 120


dash_app  = dash.Dash(__name__,\
                      use_pages=True,\
                      external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash_app.server    

# app.layout = html.Div([
    
#     dcc.Store(id="store_Demand_01", data = Demand_Electricity_Texas.to_json() ),
#     dcc.Store(id="store_Demand_02", data = Demand_Electricity_TexasForecast.to_json() ),

#  	html.H1('Multi-page app with Dash Pages'),

#     html.Div(
#         [
#             html.Div(
#                 dcc.Link(
#                     f"{page['name']} - {page['path']}", href=page["relative_path"]
#                 )
#             )
#             for page in dash.page_registry.values()
#         ]
#     ),

#  	dash.page_container
# ])

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Multi Page App Demo",
    color="primary",
    dark=True,
    className="mb-2",
)

dash_app.layout = dbc.Container([
    
    dcc.Store(id="store_Demand_01", data = Demand_Electricity_Texas.to_json() ),
    dcc.Store(id="store_Demand_02", data = Demand_Electricity_TexasForecast.to_json() ),

    navbar, 
    dash.page_container
    
    ],
    fluid=True,
)

######################################3

if __name__ == '__main__':
    
    
    dash_app.run_server(debug=True)
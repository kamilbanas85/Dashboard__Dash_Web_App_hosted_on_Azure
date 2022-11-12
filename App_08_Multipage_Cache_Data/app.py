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


from flask_caching import Cache


#%%

# MainDirectory = os.path.abspath(os.path.dirname(__file__))
# os.chdir(MainDirectory)

#%%

# from Download_And_Porcess_Data import Download_And_Process_Data


# ResultsDIC = Download_And_Process_Data(Authenication = 'trusted', returnData = True)

# # Authenication =  'trusted'  or  'password'  or  'trusted-azure'

# #%%

# for key,val in ResultsDIC.items():
#       exec(key + '=val')


# # HistoryTotal_30m
# # HistoryTotal_1d



#############################################################################
#############################################################################
#%%

# LayoutRefreshTimeInMin = 120


dash_app  = dash.Dash(__name__,\
                      use_pages=True,\
                      external_stylesheets=[dbc.themes.BOOTSTRAP])

app = dash_app.server    


#%%



navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Analysis Type",
        toggle_style={"color": "white",  "backgroundColor":"blue"}
        
    ),
    
    brand="Bitcoin",
    color="primary",
    dark=True,
    # className="mb-2",
    fluid = True,
    #style={'font-family': 'Times New Roman'}
)

dash_app.layout = dbc.Container([
    

    navbar, 
    dash.page_container
    
    ],
    fluid=True,
)

######################################3

if __name__ == '__main__':
    
    
    dash_app.run_server(debug=True, use_reloader = False)
import numpy as np
import pandas as pd

import pyodbc
from retry import retry


#####################################################

def GetConnStr(ServerName: str, DBname: str, Driver: str,\
               Authenication: str = 'trusted',\
               UserName: str = 'UserName', Password: str= 'Password') -> str:
    
    # Authenication =  'trusted'  or  'password'  or  'trusted-azure'
    
    BaiscConnStr = 'Driver=' + Driver +\
                   ';Server=' + ServerName +\
                   ';PORT=1443' +\
                   ';Database=' + DBname                
          
    if Authenication =='trusted':
          ConnStr = BaiscConnStr +\
                     ";Trusted_Connection=yes"

    elif  Authenication == 'trusted-azure':
          ConnStr = BaiscConnStr +\
                     ";Authentication=ActiveDirectoryMsi"

    elif  Authenication == 'password':
          ConnStr = BaiscConnStr +\
                     ";UID=" + UserName +\
                     ";PWD=" + Password

    return ConnStr
 

##############################################################################################################

@retry(tries=3, delay=60)
def Download_Data_From_AzureDB(querySQL: str = '', Authenication: str = 'trusted') -> pd.DataFrame:
    
    
    ServerName = 'dashboard-dbserver01.database.windows.net'
    DBname = 'baza01'
    Driver= '{ODBC Driver 17 for SQL Server}'
    UserName = 'kamilbanas85'
    Password = 'XXX'
    
    # Authenication =  'trusted'  or  'password'  or  'trusted-azure'
    connStr = GetConnStr( ServerName, DBname, Driver, Authenication, UserName, Password)
    conn = pyodbc.connect( connStr )

    with conn:
        data = pd.read_sql_query( querySQL,  conn)     
      
    
    return data
 

        
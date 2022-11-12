# Dash App hosted on Azure - automatic data update from SQL Server

Repository contains examples of a Dash web app hosted on AZURE as the 'Azure Web Apps'. Examples show a basic plot and different methods automatic data updating from SQL server:
 - Interval Component
 - BackgroundScheduler

A different methods of transfer data between components were used:
 - Store component
 - ServerSideOutput
 - Saving files into disk file.
 
 MuliPage app examples show 2 diffrent aproach to transfer data beteen pages:
 - using dcc.Store element - can be extended to ServerSideOutput
 - using Cache

'Libraries_List' file contains most common libraries list ( 'dash-extensions' require  '--use-feature=2020-resolver' )
requirements.txt <- requirement file related to libraries list from a file 'Libraries_List'

!!!!!!!!!!!!!
When automatic update is app is deplyed, it requires turn on 'Always on'
    Configuration -> General Settings -> Always on
!!!!!!!!!!!!!

import numpy as np
import pandas as pd

import datetime


#%%

def prepare_data_perGasYear( DataHistory, nrOfYearsToReturn = 2 ):
    
     
    #######################################################################################    
    # Base Data - create dictionary -  'columnName': 'DataFrame with data for columnName'
    
    GasYearDIC = {}

    for var in DataHistory.columns:
        
       DF = DataHistory[[var]].copy()

       DF = DF.assign(GasYear_par1 = lambda x: np.where( (x.index.month >= 1) &  (x.index.month <= 9),  x.index.year-1, x.index.year),
                      GasYear_par2 = lambda x: np.where( (x.index.month >= 1) &  (x.index.month <= 9),  x.index.year, x.index.year+1),
                      GasYear = lambda x: x['GasYear_par1'].astype('str') + '/' + x['GasYear_par2'].astype('str'),
                      MonthDay = lambda x: x.index.strftime('%m-%d') )
              
       Last5yearsStatistics = DF.copy().assign(MaxYear = lambda x: max(x['GasYear_par1']))\
                                       .query('MaxYear - GasYear_par1 >= 1 & MaxYear - GasYear_par1 <= 5 ')\
                                       .groupby('MonthDay')\
                                       .agg( min_5years = pd.NamedAgg(var, "min"),
                                             avg_5years = pd.NamedAgg(var, "mean"),
                                             max_5years = pd.NamedAgg(var, "max") )
               
       # Reshape to get column as gas year  
       DFperGasYear =  DF.pivot_table(index = ['MonthDay'], columns ='GasYear', values = var)\
                                                .rename_axis(None,axis = 1)
       # Add statiscts                                          
       DFperGasYear = DFperGasYear.iloc[:,-(nrOfYearsToReturn + 1):]\
                                  .join(Last5yearsStatistics, how='left', on = 'MonthDay')
       # Remove 29.02
       DFperGasYear.drop(["02-29"], inplace = True)  
       
       #Channge order to start from 01-10
       DFperGasYear = DFperGasYear.loc['10-01':].append(DFperGasYear.loc[:'10-01'].iloc[:-1])

       
       GasYearDIC[var] = DFperGasYear


    return GasYearDIC


#%%

def prepare_data_perYear( DataHistory, nrOfYearsToReturn = 2  ):
    
     
    #######################################################################################    
    # Base Data - create dictionary -  'columnName': 'DataFrame with data for columnName'
    
    YearDIC = {}

    for var in DataHistory.columns:
        
       DF = DataHistory[[var]].copy()

       DF = DF.assign(Year = lambda x: x.index.year,\
                      MonthDay = lambda x: x.index.strftime('%m-%d') )
              
       Last5yearsStatistics = DF.copy().assign(MaxYear = lambda x: max(x['Year']))\
                                       .query('MaxYear - Year >= 1 & MaxYear - Year <= 5 ')\
                                       .groupby('MonthDay')\
                                       .agg( min_5years = pd.NamedAgg(var, "min"),
                                             avg_5years = pd.NamedAgg(var, "mean"),
                                             max_5years = pd.NamedAgg(var, "max") )
               
       # Reshape to get column as gas year  
       DFperYear =  DF.pivot_table(index = ['MonthDay'], columns ='Year', values = var)\
                                                .rename_axis(None,axis = 1)
       # Add statiscts                                          
       DFperYear = DFperYear.iloc[:,-(nrOfYearsToReturn + 1):]\
                                  .join(Last5yearsStatistics, how='left', on = 'MonthDay')
       # Remove 29.02
       DFperYear.drop(["02-29"], inplace = True)  
       
       YearDIC[var] = DFperYear


    return YearDIC
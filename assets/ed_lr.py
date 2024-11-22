# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:47:13 2024

@author: win11
"""

import os
import sys
import numpy as np
import pandas as pd
from pandas import Period
import math
from sklearn.linear_model import LinearRegression

#https://www.kaggle.com/code/ryanholbrook/linear-regression-with-time-series


def create_linear_regr_pred(services,df_in, granularity):
    

    df = df_in.tail(156).copy(deep=True)
    #df.drop(df.head(89).index,inplace = True)
    df['Time'] = np.arange(len(df.index))

    df_out = pd.DataFrame()
    ## tail 156 is more or less the last 3 years
    number_of_weeks = 156
    df_out['Date'] = df_in.tail(number_of_weeks)['Date']

    values_toadd_1y = []
    values_toadd_2y = []

    # Training data
    X = df.loc[:, ['Time']]  # features
    
    for x in services['Service']:
           postpan = x+"_sum_tot_postpan"
           y = df.loc[:, postpan]  # target

           # Train the model
           model = LinearRegression()
           model.fit(X, y)

            # Store the fitted values as a time series with the same time index as
            # the training data
           y_pred = pd.Series(model.predict(X), index=X.index)
           
           df_out[x + "_pred"] = y_pred

           
           #in 1 year (+52weeks), + 2 years
           
           new_data = [number_of_weeks + 52,number_of_weeks+104]  


           new_data_as_frame = pd.DataFrame(new_data, columns=["Time"])


           predicted_values = model.predict(new_data_as_frame )
           
           #add two prediction values (1 year, 2 year to services df)
           #in 1 year, in 2 years
           
           values_toadd_1y.append(predicted_values[0])
           values_toadd_2y.append(predicted_values[1])
           
           

    match granularity:
         case 'weekdays':
                       services['pred_1y_weekdays'] = pd.Series(values_toadd_1y)
                       services['pred_2y_weekdays'] = pd.Series(values_toadd_2y)
                       
         case 'weekend':
                       services['pred_1y_weekend'] = pd.Series(values_toadd_1y)
                       services['pred_2y_weekend'] = pd.Series(values_toadd_2y)
         case _:  
                       services['pred_1y'] = pd.Series(values_toadd_1y)
                       services['pred_2y'] =  pd.Series(values_toadd_2y)        

        


    #df_out has the linear regressions results for the last 3 years
    #for all services, going to merge these with the data yw dataframes
    
    df_in = df_in.merge(df_out, how='left')
    
    
    #replace nan's (the rows with no predictions attached) with zeroes for all predicted columns
    
    cols = ["All_pred","Subways_pred","Buses_pred","LIRR_pred","Metro_North_pred", 
            "Access_A_Ride_pred", "Bridges_and_Tunnels_pred", "Staten_Island_Railway_pred"]
    df_in[cols] = df_in[cols].fillna(0)
    
    
    
    
    
    



    return services,df_in
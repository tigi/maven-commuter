# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:42:48 2024

@author: win11
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:32:24 2024

@author: vraag
"""
##READ DATAFILES##

# get temp working directory

#import os
import sys
import numpy as np
import pandas as pd
#from pandas import Period
import math
import assets.ed_lr as elr




def data_elt ():
       
    

    #import & process data
    df_ridership_raw= read_ridership_csv()
    df_ridership_all = df_ridership_raw.copy(deep=True)
    df_ridership_all = rename_columns(df_ridership_all)
    df_ridership_all = df_add_dateinfo(df_ridership_all)
    df_ridership_all = df_add_prepan_totals(df_ridership_all)
    df_ridership_all = df_replace_zero_values_prepan_tot (df_ridership_all)
    df_ridership_all = df_add_allservices_totals(df_ridership_all)
    
    
    
    #df_ridership_ym = df_create_all_grouping_year_month(df_ridership_all)
    
    df_ridership_yw = df_create_all_grouping_year_week(df_ridership_all)
     
    
    df_ridership_yw_weekend, df_ridership_yw_weekdays = df_create_all_grouping_year_week_splitter(df_ridership_all)
    
    
     
    
    #import services descriptive csv file
    df_services = read_services_csv()
    #max boundaries is used for the ymax yaxes visuals
    df_services = add_max_boundaries_per_service_weekly(df_services, df_ridership_yw,df_ridership_yw_weekend,df_ridership_yw_weekdays)
    #avg last 52 weeks of predicted (last 365 days for ridership_all) is to decide on the background color of the 2years row in trend totals,
    # compare prediction to avg over last 3 years this is horrible but fast.
    
    
    
    df_ridership_yw = create_postpan_perc_prepan (df_services, df_ridership_yw)
    df_ridership_yw_weekdays = create_postpan_perc_prepan (df_services, df_ridership_yw_weekdays)
    df_ridership_yw_weekend = create_postpan_perc_prepan (df_services, df_ridership_yw_weekend )
    
    #average prepan
    df_services = add_avg_sum_tot_prepan_last_year(df_services, df_ridership_yw, df_ridership_yw_weekdays, df_ridership_yw_weekend)


    df_services= what_color_has_my_trend (df_services, df_ridership_yw,df_ridership_yw_weekdays,df_ridership_yw_weekend)
     
    
    df_services, df_ridership_yw = elr.create_linear_regr_pred(df_services, df_ridership_yw, '')
    df_services,df_ridership_yw_weekdays = elr.create_linear_regr_pred(df_services, df_ridership_yw_weekdays,'weekdays')
    df_services,df_ridership_yw_weekend = elr.create_linear_regr_pred(df_services, df_ridership_yw_weekend,'weekend')
    
    
    df_services = what_color_has_my_trend_in2years(df_services, df_ridership_yw,df_ridership_yw_weekend,df_ridership_yw_weekdays)
    
    
    #gonna write them all 4 dataframes to a csv for import in the app
    
    
    
    df_services.to_csv('services_new.csv', index=False)
    df_ridership_yw.to_csv('ridership_yw.csv', index=False)
    df_ridership_yw_weekdays.to_csv('ridership_yw_weekdays.csv', index=False)
    df_ridership_yw_weekend.to_csv('ridership_yw_weekend.csv', index=False)
    
    
    
        
    
    return df_services, df_ridership_yw, df_ridership_yw_weekdays, df_ridership_yw_weekend


    


def read_ridership_csv():
    #os.chdir('d:\\studie\\data-maven\\maven-ridership\\mta+daily+ridership')
    fname = 'MTA_Daily_Ridership.csv'
    try:
        f = open(fname, 'rb')
    except OSError:
        print ("Could not open/read file:", fname)
        sys.exit()
    with f:
       raw_data = pd.read_csv(fname)
       return raw_data

    
#services is a configuration and descriptive file for services

def read_services_csv():
    fname = 'Services.csv'
    try:
        f = open(fname, 'rb')
    except OSError:
        print ("Could not open/read file:", fname)
        sys.exit()
    with f:
       raw_data = pd.read_csv(fname)
       return raw_data
 
       
   
def rename_columns(df_in):
    map_names = {
        "Subways: Total Estimated Ridership" : "Subways_tot_postpan",         
        'Subways: % of Comparable Pre-Pandemic Day' : 'Subways_tot_prepan_perc',        
        'Buses: Total Estimated Ridership' : 'Buses_tot_postpan',         
        'Buses: % of Comparable Pre-Pandemic Day' : 'Buses_tot_prepan_perc',         
        'LIRR: Total Estimated Ridership' : 'LIRR_tot_postpan',         
        'LIRR: % of Comparable Pre-Pandemic Day' : 'LIRR_tot_prepan_perc',         
        'Metro-North: Total Estimated Ridership' : 'Metro_North_tot_postpan',         
        'Metro-North: % of Comparable Pre-Pandemic Day' : 'Metro_North_tot_prepan_perc',         
        'Access-A-Ride: Total Scheduled Trips' :'Access_A_Ride_tot_postpan' ,
        'Access-A-Ride: % of Comparable Pre-Pandemic Day' : 'Access_A_Ride_tot_prepan_perc',         
        'Bridges and Tunnels: Total Traffic' :'Bridges_and_Tunnels_tot_postpan' ,         
        'Bridges and Tunnels: % of Comparable Pre-Pandemic Day' :'Bridges_and_Tunnels_tot_prepan_perc' ,         
        'Staten Island Railway: Total Estimated Ridership' :'Staten_Island_Railway_tot_postpan' ,        
        'Staten Island Railway: % of Comparable Pre-Pandemic Day' : 'Staten_Island_Railway_tot_prepan_perc'
        }
    df_in.rename(columns = map_names, inplace = True)
    return df_in

def df_add_dateinfo(df_in):
    ## change datatypes, all integers except date, convert date, remove timepart (does not work well), add day of week
    ##correct de date for yearchanges and grouper

    df_in['Date']= pd.to_datetime(df_in['Date']) - pd.to_timedelta(7, unit='d')
    df_in['Year'] = df_in['Date'].dt.year
    df_in['Month'] = df_in['Date'].dt.month
    df_in['DoW'] = df_in['Date'].dt.dayofweek #o is monday
    df_in['IsWeekday']= np.where(df_in['DoW'] < 5, True, False)

    
 
    
    df_in.drop(df_in.head(1).index,inplace = True)
    #remove last 5 records, incomplete week
    df_in.drop(df_in.tail(4).index,inplace = True)
    
    return(df_in)



def df_add_prepan_totals(df_in):
    #calculate prepan in numbers based on subway as percentage prepan.
    ##division by zero!!!!!!!! en ik wil er nog overall totalen bij
    df_in['Subways_tot_prepan'] = 100*(df_in['Subways_tot_postpan']/df_in['Subways_tot_prepan_perc'])
    df_in['Buses_tot_prepan'] = 100*(df_in['Buses_tot_postpan']/df_in['Buses_tot_prepan_perc'])
    df_in['LIRR_tot_prepan'] = 100*(df_in['LIRR_tot_postpan']/df_in['LIRR_tot_prepan_perc'])
    df_in['Metro_North_tot_prepan'] = 100*(df_in['Metro_North_tot_postpan']/df_in['Metro_North_tot_prepan_perc'])
    df_in['Access_A_Ride_tot_prepan'] = 100*(df_in['Access_A_Ride_tot_postpan']/df_in['Access_A_Ride_tot_prepan_perc'])
    df_in['Bridges_and_Tunnels_tot_prepan'] = 100*(df_in['Bridges_and_Tunnels_tot_postpan']/df_in['Bridges_and_Tunnels_tot_prepan_perc'])
    df_in['Staten_Island_Railway_tot_prepan'] = np.where(df_in['Staten_Island_Railway_tot_prepan_perc'] >= 1, \
                                                100*(df_in['Staten_Island_Railway_tot_postpan']/df_in['Staten_Island_Railway_tot_prepan_perc']), \
                                                0)
        
    return df_in

def df_replace_zero_values_prepan_tot (df_in):
    #going to replace these pre-pandemic estimates with the date+365 values
    #not completely correct but good enough
    mean_weekend = df_in.query('IsWeekday==False')['Staten_Island_Railway_tot_prepan'].mean()
    df_in['Staten_Island_Railway_tot_prepan'] = df_in['Staten_Island_Railway_tot_prepan'].replace(0,mean_weekend)
        
    return df_in





def df_add_allservices_totals(df_in):
    #calculate the all services together columns
    list_cols_prepan = ['Subways_tot_prepan','Buses_tot_prepan','LIRR_tot_prepan','Metro_North_tot_prepan','Access_A_Ride_tot_prepan','Bridges_and_Tunnels_tot_prepan','Staten_Island_Railway_tot_prepan']
    df_in['All_tot_prepan'] = df_in.loc[:,list_cols_prepan].sum(axis = 1)
    list_cols_postpan = ['Subways_tot_postpan','Buses_tot_postpan','LIRR_tot_postpan','Metro_North_tot_postpan','Access_A_Ride_tot_postpan','Bridges_and_Tunnels_tot_postpan','Staten_Island_Railway_tot_postpan']
    df_in['All_tot_postpan'] = df_in.loc[:,list_cols_postpan].sum(axis = 1)
    return df_in




def df_create_all_grouping_year_week(df_in):
    
    df_out = df_in.copy(deep=True)
    df_out = df_out.groupby([pd.Grouper(key='Date', freq='W')]).agg(        
        #Label = ('Label_yw', 'max'),

        All_sum_tot_postpan = ('All_tot_postpan', 'sum'),
        All_sum_tot_prepan = ('All_tot_prepan', 'sum'),
        Subways_sum_tot_postpan = ('Subways_tot_postpan', 'sum'),
        Subways_sum_tot_prepan =('Subways_tot_prepan', 'sum'),
        Buses_sum_tot_postpan = ('Buses_tot_postpan', 'sum'),
        Buses_sum_tot_prepan = ('Buses_tot_prepan', 'sum'),
        LIRR_sum_tot_postpan = ('LIRR_tot_postpan', 'sum'),
        LIRR_sum_tot_prepan = ('LIRR_tot_prepan', 'sum'),
        Metro_North_sum_tot_postpan = ('Metro_North_tot_postpan', 'sum'),
        Metro_North_sum_tot_prepan = ('Metro_North_tot_prepan', 'sum'),
        Access_A_Ride_sum_tot_postpan = ('Access_A_Ride_tot_postpan', 'sum'),
        Access_A_Ride_sum_tot_prepan = ('Access_A_Ride_tot_prepan', 'sum'),
        Bridges_and_Tunnels_sum_tot_postpan = ('Bridges_and_Tunnels_tot_postpan', 'sum'),
        Bridges_and_Tunnels_sum_tot_prepan = ('Bridges_and_Tunnels_tot_prepan', 'sum'),
        Staten_Island_Railway_sum_tot_postpan = ('Staten_Island_Railway_tot_postpan', 'sum'),
        Staten_Island_Railway_sum_tot_prepan = ('Staten_Island_Railway_tot_prepan', 'sum'),
        ).reset_index()
    


    return df_out






def df_create_all_grouping_year_week_splitter(df_in):
    
    df_weekend = df_in.query('IsWeekday==False')
    df_weekend = df_weekend.groupby([pd.Grouper(key='Date', freq='W')]).agg(        

        All_sum_tot_postpan = ('All_tot_postpan', 'sum'),
        All_sum_tot_prepan = ('All_tot_prepan', 'sum'),
        Subways_sum_tot_postpan = ('Subways_tot_postpan', 'sum'),
        Subways_sum_tot_prepan = ('Subways_tot_prepan', 'sum'),
        Buses_sum_tot_postpan = ('Buses_tot_postpan', 'sum'),
        Buses_sum_tot_prepan = ('Buses_tot_prepan', 'sum'),
        LIRR_sum_tot_postpan = ('LIRR_tot_postpan', 'sum'),
        LIRR_sum_tot_prepan = ('LIRR_tot_prepan', 'sum'),
        Metro_North_sum_tot_postpan = ('Metro_North_tot_postpan', 'sum'),
        Metro_North_sum_tot_prepan = ('Metro_North_tot_prepan', 'sum'),
        Access_A_Ride_sum_tot_postpan = ('Access_A_Ride_tot_postpan', 'sum'),
        Access_A_Ride_sum_tot_prepan = ('Access_A_Ride_tot_prepan', 'sum'),
        Bridges_and_Tunnels_sum_tot_postpan = ('Bridges_and_Tunnels_tot_postpan', 'sum'),
        Bridges_and_Tunnels_sum_tot_prepan = ('Bridges_and_Tunnels_tot_prepan', 'sum'),
        Staten_Island_Railway_sum_tot_postpan = ('Staten_Island_Railway_tot_postpan', 'sum'),
        Staten_Island_Railway_sum_tot_prepan = ('Staten_Island_Railway_tot_prepan', 'sum'),
        ).reset_index()

    
    df_weekdays = df_in.query('IsWeekday==True')
    df_weekdays = df_weekdays.groupby([pd.Grouper(key='Date', freq='W')]).agg(        

        All_sum_tot_postpan = ('All_tot_postpan', 'sum'),
        All_sum_tot_prepan = ('All_tot_prepan', 'sum'),
        Subways_sum_tot_postpan = ('Subways_tot_postpan', 'sum'),
        Subways_sum_tot_prepan = ('Subways_tot_prepan', 'sum'),
        Buses_sum_tot_postpan = ('Buses_tot_postpan', 'sum'),
        Buses_sum_tot_prepan = ('Buses_tot_prepan', 'sum'),
        LIRR_sum_tot_postpan = ('LIRR_tot_postpan', 'sum'),
        LIRR_sum_tot_prepan = ('LIRR_tot_prepan', 'sum'),
        Metro_North_sum_tot_postpan = ('Metro_North_tot_postpan', 'sum'),
        Metro_North_sum_tot_prepan = ('Metro_North_tot_prepan', 'sum'),
        Access_A_Ride_sum_tot_postpan = ('Access_A_Ride_tot_postpan', 'sum'),
        Access_A_Ride_sum_tot_prepan = ('Access_A_Ride_tot_prepan', 'sum'),
        Bridges_and_Tunnels_sum_tot_postpan = ('Bridges_and_Tunnels_tot_postpan', 'sum'),
        Bridges_and_Tunnels_sum_tot_prepan = ('Bridges_and_Tunnels_tot_prepan', 'sum'),
        Staten_Island_Railway_sum_tot_postpan = ('Staten_Island_Railway_tot_postpan', 'sum'),
        Staten_Island_Railway_sum_tot_prepan = ('Staten_Island_Railway_tot_prepan', 'sum'),
        ).reset_index()

    return df_weekend,df_weekdays

def create_postpan_perc_prepan (services, df_in):
    #these values are calculated again instead of a mean of a sum of percentages
    #because 10% of a very high number can be much more than 90% of a small number
      
       for x in services['Service']:
           prepan = x+"_sum_tot_prepan"
           postpan = x + "_sum_tot_postpan"
           columnname = x + "_perc_postpan_as_prepan"
           df_in[columnname] = round((100 * df_in[postpan]) / df_in[prepan],0)
    
       return df_in
    

def add_max_boundaries_per_service_weekly(df_in, df_week, df_weekend, df_weekdays):
   #max are based on a service both predicted pre and estimated real
   #in the weekly grouped summary, but also week and weekend min is always 0
   

   #need them for all three variations to get the absolute max in a visual
   #list_avg_max_values = []
   list_sum_max_values = []
   
   for x in df_in['Service']:

       
       list_sum_max_services = []
       prepan = x+"_sum_tot_prepan"
       postpan = x + "_sum_tot_postpan"
       round_up = df_in[df_in['Service']==x]['Format_number_sum'].values[0]
       list_sum_max_services.append(max(df_week[prepan].max(),df_week[postpan].max()))
       list_sum_max_services.append(max(df_weekend[prepan].max(),df_weekend[postpan].max()))
       list_sum_max_services.append(max(df_weekdays[prepan].max(),df_weekdays[postpan].max()))
       max_all = max(list_sum_max_services)
       if round_up == 'M':
           max_all = int(math.ceil(max_all / 1000000.0)) * 1000000
       elif round_up == 'K50':
           max_all = int(math.ceil(max_all / 50000.0)) * 50000
       else:
           max_all = int(math.ceil(max_all / 10000.0)) * 10000
           
       list_sum_max_values.append(max_all)
       

   df_in['sum_max_value'] = list_sum_max_values

    
    
   return df_in 



def add_avg_sum_tot_prepan_last_year(services, ridership_yw, ridership_weekdays, ridership_weekend) : 
    
    #based on the all table containing all sums, the mean for the last year pre-pandemic is calculated
    
    newcolumns = ['prepan_avg_lastyear', 'prepan_avg_lastyear_weekdays' , 'prepan_avg_lastyear_weekend' ]
    
    for columnname in newcolumns:
        
        
        values_toappend = []  
        
               
        #match colorpredition with the correct colum for the formula
         
    
        for x in services['Service']:
            
            match columnname: 
                case 'prepan_avg_lastyear': 
                    values_toappend.append(ridership_yw.tail(52)[x + '_sum_tot_prepan'].mean())
                case 'prepan_avg_lastyear_weekdays':
                    values_toappend.append( ridership_weekdays.tail(52)[x + '_sum_tot_prepan'].mean())
                case 'prepan_avg_lastyear_weekend':
                    values_toappend.append(ridership_weekend.tail(52)[x + '_sum_tot_prepan'].mean())

        
            #active_service = services.query("Service == @x")
            #.loc[row_indexer,col_indexer], the order will be the
            #order services have in df_services

            

            
        
        
            #all (weekdays + weekends)

              

    
    
    
        services[columnname ] =pd.Series(values_toappend)

        
        
    
    return services


def what_color_has_my_trend (df_services,in_yw, in_yw_weekdays, in_yw_weekend):
    #color/trend decision is based on percentages (post as perc of pre)

    list_colors=['g','o','r']
    
    new_columns = ['yw_trendcolor', 'yw_weekdays_trendcolor', 'yw_weekend_trendcolor']
    
    
    
    for column in new_columns: 
        values_colors = []
        
        match column:
            case 'yw_trendcolor':
                df_in = in_yw
            case 'yw_weekdays_trendcolor':
                df_in = in_yw_weekdays
            case  'yw_weekend_trendcolor':
                df_in = in_yw_weekend
    
    
    
        #last 52 weeks of dataframe
        df_processing = df_in.tail(52)
        #list = [g,o,r] values (green, orange, red)
        for x in df_services['Service']:
            
            list_colornumbers = []
            col_tocheck = x + "_perc_postpan_as_prepan"
        

            #values out of 52 larger than 95
            df_bool = (df_processing[col_tocheck] >= 100)
            list_colornumbers.append(df_bool.sum().sum().item() )
            df_bool = (df_processing[col_tocheck] >= 80)
            list_colornumbers.append(df_bool.sum().sum().item() )
            df_bool = (df_processing[col_tocheck] < 80)
            list_colornumbers.append(df_bool.sum().sum().item() )
        #print(f"{x} :")
        #print(list_colornumbers)
        #find first occurence in list larger than 42 = approx 90% larger than 100% in last year.
        
            try:
            #find the index of the first list item where 26 or more weeks are above value
            #if out of index, use index 2 which means red thus meaning no situation where
            #42 or more weeks showed minimal of 75% recovery
                index_max = [ n for n,i in enumerate(list_colornumbers) if i>25 ][0]
            except:
            #red
                index_max = 2
                
            values_colors.append(list_colors[index_max])
                
        
        df_services[column] = pd.Series(values_colors)
        
        
        #print(index_max)
        #print(f"color:{list_colors[index_max]}")
         
    
    
    return df_services




def what_color_has_my_trend_in2years (services, ridership_yw,ridership_yw_weekend,ridership_yw_weekdays):
    #color/trend decision is based value in 2 years over average last 3 years
    #I know this is so wrong :-)
    
    #last 52 weeks of dataframe

    #list = [g,o,r] values (green, orange, red)
    
    #compare for each service/granulariy the prediction in 2 years vs avg pre-pandemic last 52 weeks
    #services _pred_2y vs prepan_avg_lastyear, store result as colorcode in services table
    
    
    newcolumns = ['pred_color_yw1','pred_color_yw2','pred_color_yw_weekdays1','pred_color_yw_weekdays2',\
                  'pred_color_yw_weekend1','pred_color_yw_weekend2']
        
        
        
        
        
    for columnname in newcolumns:
        #print(columnname)
        
        values_toappend = []  
        #print(values_toappend)
               
        #match colorprediCtion with the correct colum for the formula
        match columnname: 
            case 'pred_color_yw1': 
                y = 'pred_1y'
                p = 'prepan_avg_lastyear'
            case 'pred_color_yw2':
                y = 'pred_2y'
                p = 'prepan_avg_lastyear'
            case 'pred_color_yw_weekdays1':
                y ='pred_1y_weekdays'
                p = 'prepan_avg_lastyear_weekdays'
            case 'pred_color_yw_weekdays2':
                y ='pred_2y_weekdays'
                p = 'prepan_avg_lastyear_weekdays'
            case 'pred_color_yw_weekend1':
                y = 'pred_1y_weekend'
                p = 'prepan_avg_lastyear_weekend'
            case 'pred_color_yw_weekend2':
                y = 'pred_2y_weekend'
                p = 'prepan_avg_lastyear_weekend'
    
    
        for x in services['Service']:
 
            
            
        
            #active_service = services.query("Service == @x")
            #.loc[row_indexer,col_indexer], the order will be the
            #order services have in df_services

    
            
            values_toappend.append(get_pred_color(services.loc[services['Service'] == x][y].item(),services.loc[services['Service'] == x][p].item()))
            
        
        
            #all (weekdays + weekends)

            
        services[columnname] = pd.Series(values_toappend)
    
    return services



def get_pred_color(a,b):
    
        #returns the color based on comparison between a (prediction in 2 years) and b (avg last 52 weeks) 

        
        if float(a) > float(b):
                #green
                pred_color = "#70d158"
        elif float(a) > float(.8*b):
                #orange
                pred_color = "#f2870c"
        else : 
                #red
                pred_color = "#e33636"
        
    
        return pred_color



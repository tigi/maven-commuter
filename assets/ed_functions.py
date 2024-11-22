# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:59:19 2024

@author: win11
"""

from dash import  html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import assets.ed_text as edt
import assets.ed_style as eds



def create_services_options(df_in):
    
    #returns the dropdown options for services in html format
    #based on services in the df_services tabel
    
    
    options_dict = dict(zip(df_in['Service_Label'], df_in['Service']))
    options = [{'label':label,'value':waarde} for label, waarde in options_dict.items()]
    return options

def create_general_information_card(service,df_services):
    
    #collects & outputs the service description (from df_services) in an accordeon item
    
    service_description = df_services[df_services['Service']==service]['Service_Description'].values[0]
    card = html.P(f"{service_description}", className="card-text")

    return card

def create_data_information_card(service,df_services):
    
    #collects & outputs the datacollect description (from df_services) in an accordeon item
    
    
    service_datacollection = df_services[df_services['Service']==service]['Service_datacollection'].values[0]
    card = html.P(f"{service_datacollection}", className="card-text")
    return card


def update_card_performance_expectations(service,services, ridership_yw, ridership_yw_weekdays, ridership_yw_weekend,view):
    
    
    #collects the data for the totals overview

    #roundup dict gets the formats (K,M) for the services to use when rounding to 2 decimals
    roundup_dict =  pd.Series(services.Format_number_sum.values,index=services.Service).to_dict()
    
    #maxdate is the date of the last row in the df. It is used on screen as a reference for 
    #1 year from, 2 year from and used for the actual value in the last week
    
    maxdate = ridership_yw['Date'].max().strftime("%b %d, %Y")
    
    #get last values from the trendline, based on granularity (allweek, weekdays, weekend)
    #granularity = chosen dataframe as input.
    xnow_yw, ynow_yw = get_last_trendline_xy(ridership_yw, service)
    xnow_yw_weekdays, ynow_yw_weekdays = get_last_trendline_xy(ridership_yw_weekdays, service)
    xnow_yw_weekend, ynow_yw_weekend = get_last_trendline_xy(ridership_yw_weekend, service)
    
    #round these values 
    f_ynow_yws  = format_number_screenready(ynow_yw,roundup_dict.get(service))
    f_ynow_yw_weekdays =  format_number_screenready(ynow_yw_weekdays,roundup_dict.get(service))
    f_ynow_yw_weekend = format_number_screenready(ynow_yw_weekend,roundup_dict.get(service))
    
    #columns <servicename> + _pred_1y & _pred_2y in df_services (none, _weekdays & _weekend)
    #seach for the row with the service and the values, 6 values
    
    #get index of service in services
    
    
    #get the row for this service, extract the prediction columns
    
    cols_predictions=['pred_1y', 'pred_1y_weekdays', 'pred_1y_weekend',\
                      'pred_2y', 'pred_2y_weekdays', 'pred_2y_weekend',
                      'pred_color_yw1', 'pred_color_yw_weekdays1',  'pred_color_yw_weekend1',
                      'pred_color_yw2', 'pred_color_yw_weekdays2',  'pred_color_yw_weekend2',
                      ]
    active_service = services.query("Service == @service")[cols_predictions]
    #print(active_service.info() )
    
    #get values trend one year from now

    f_y1_yws  = format_number_screenready(active_service.iloc[0]['pred_1y'],roundup_dict.get(service))
    f_y1_yw_weekdays =  format_number_screenready(active_service.iloc[0]['pred_1y_weekdays'],roundup_dict.get(service))
    f_y1_yw_weekend = format_number_screenready(active_service.iloc[0]['pred_1y_weekend'],roundup_dict.get(service))

     #get values trend two years from now

    f_y2_yws  = format_number_screenready(active_service.iloc[0]['pred_2y'],roundup_dict.get(service))
    f_y2_yw_weekdays =  format_number_screenready(active_service.iloc[0]['pred_2y_weekdays'],roundup_dict.get(service))
    f_y2_yw_weekend = format_number_screenready(active_service.iloc[0]['pred_2y_weekend'],roundup_dict.get(service))

        
    
    table_header_prediction = [
        html.Thead(html.Tr([html.Th(""),html.Th("Overall"), html.Th("Weekdays"), html.Th("Weekends")]))
    ]
    
    
    #Insert the values into the table
    color_all1 = active_service['pred_color_yw1']
    color_weekend1 = active_service['pred_color_yw_weekend1']
    color_weekdays1 = active_service['pred_color_yw_weekdays1']
    color_all2 = active_service['pred_color_yw2']
    color_weekend2 = active_service['pred_color_yw_weekend2']
    color_weekdays2 = active_service['pred_color_yw_weekdays2']
    
    servicelabel = get_service_label(services,service)
    
    
    row_prediction1 = html.Tr([html.Td(f"{maxdate}"),\
                      html.Td(f"{f_ynow_yws}"),\
                      html.Td(f"{f_ynow_yw_weekdays}"),\
                      html.Td(f"{f_ynow_yw_weekend}")])    

    row_prediction2 = html.Tr([html.Td("In 1 year"),\
                      html.Td(f"{f_y1_yws}", style = {"color":"#222", "backgroundColor": color_all1}),\
                      html.Td(f"{f_y1_yw_weekdays}", style = {"color":"#222","backgroundColor": color_weekdays1}),\
                      html.Td(f"{f_y1_yw_weekend}", style = {"color":"#222","backgroundColor": color_weekend1})])  
    row_prediction3 = html.Tr([html.Td("In 2 years", style={"fontWeight":"bold"}),\
                      html.Td(f"{f_y2_yws}" , style = {"fontWeight":"bold","color":"#222", "backgroundColor": color_all2}),\
                      html.Td(f"{f_y2_yw_weekdays}" , style = {"fontWeight":"bold","color":"#222","backgroundColor": color_weekdays2}),\
                      html.Td(f"{f_y2_yw_weekend}", style = {"fontWeight":"bold","color":"#222","backgroundColor": color_weekend2})])    


    table_body_prediction = [html.Tbody([row_prediction1,row_prediction2,row_prediction3 ])]

    #find additional css to show/hide the two blocks in the upperright corner, see function
    styledefvperc, styledefvsum = set_style_based_on_view(view)

    
    card = dbc.Card(
    [

        dbc.CardBody(
            [

                

                html.H2("What if this trend continues?",style = eds.style_h2()),
                edt.total_trendline_paragraph(),
                html.H3(f"Expectation ridership {servicelabel} per week", style = eds.style_h3()),
                dbc.Table(table_header_prediction + table_body_prediction, bordered=True, responsive=True,
    striped=True,) ,
                edt.numbers_explanation_cubes(),
            ]
        )], style = styledefvperc, className="margin-b-2rem"
)
    
    return card    
    
def update_card_performance_past(service, df_services,view):
    
    #create the output card for percentage view with colorcodes for 100%, 80% and worse
    
    #pimp servicename
    
        
    servicelabel = get_service_label(df_services,service)
     
    #header and image merged in one tablecell    
        
    row_recovery = html.Tr([html.Td([html.Span("Last 52"),html.Br(), html.Span("weeks")]),html.Td(["Overall",html.Br(),create_trend_icon(service,df_services,"all")]),\
                    html.Td(["Weekdays",html.Br(),create_trend_icon(service,df_services,"weekdays")]),\
                    html.Td(["Weekends",html.Br(),create_trend_icon(service,df_services,"weekend")])])


    table_body_recovery= [html.Tbody([row_recovery])]
    
    #find additional css to show/hide the two blocks in the upperright corner, see function
    styledefvperc, styledefvsum = set_style_based_on_view(view)
    
    
    
    card =dbc.Card([#this should be h2 but this is not a scss exercise
                    dbc.CardBody([
                        html.H2(f"How well did {servicelabel} recover?", style = eds.style_h2()),
                        
                        dbc.Table(table_body_recovery, bordered=True),
                        html.Br(),
                        edt.perc_explanation_icons(),
                    ]),
          ], style = styledefvsum, className="margin-b-2rem")
    
    
    return card



def create_trend_icon(service,df_service,granularity):
    #colorkeys are stored in the services table and where generated during dataprocessing.
    
    images = {'r': 'assets/no.svg', 'o' : 'assets/maybe.svg', 'g': 'assets/yes.svg' }
    alttext = {'r': 'not recovered', 'o' : '80% recovered', 'g': '100% recovered' }
    
    #the selected tab decides if we're looking @ all/weekdays/weekend
    
    match granularity:
            case "weekdays":
                column_touse = "yw_weekdays_trendcolor"
            case "weekend":
                column_touse = "yw_weekend_trendcolor"
            case _:
                column_touse = "yw_trendcolor"


    colorkey = df_service[df_service['Service']==service][column_touse].values[0]
    
    trend_icon = html.Div([
       html.Img(src=images.get(colorkey), className="arrow", alt = alttext.get(colorkey)),      
        
        ])
    
    return trend_icon
    
    
    




def get_first_trendline_xy(df_in, service):
    
    #prediction values go only back 156 weeks. 
    #trend > 0 checks for the first time a prediction is >0 (not bulletproof)
    
    #returnvalue = x,y values of first prediction
    
    trend = service + "_pred"
    index_start = df_in.query(f"{trend} > 0").index[0]         
    xstart =   df_in.iloc[index_start]['Date']  
    ystart = df_in.iloc[index_start][trend]
    
    return xstart,ystart
    
def get_last_trendline_xy(df_in, service):
    
    #prediction values go only back 156 weeks. 
    #trend > 0 checks for the first time a prediction is >0 (not bulletproof)
    
    #returnvalue = x,y values of last prediction
      
    
    trend = service + "_pred"
    index_end = len(df_in) - 1         
    xend = df_in.iloc[index_end]['Date']   
    yend = df_in.iloc[index_end][trend]
    
    return xend,yend    

def format_number_screenready(number_to_format,eenheid):
    
    #UI function to make sure the correct rounding is done to a number
    
    match eenheid:
        case 'K':
            number = str(round((number_to_format/1000),2))+'K'
        case _:
            number = str(round((number_to_format/1000000),2))+'M'
    
    return number

def set_style_based_on_view(view):
    
    
    #the right column summary switches visibility depending on the view selected
    #percentages => hide total block, totals => hide percentages block
    #works better on mobile and smaller screens
    
    match view:
        case 'vsum':
            styledefvsum = {'backgroundColor':'#222', 'display':'none'}
            styledefvperc = {'backgroundColor':'#555', 'display':'block'}
        case _:
            styledefvsum = {'backgroundColor':'#555', 'display':'block'}
            styledefvperc = {'backgroundColor':'#222', 'display':'none'}
    
    return styledefvperc, styledefvsum

def get_service_label(services,service):
    
    servicelabel = services.query("Service == @service")['Service_Label'].values[0]
   
    return servicelabel
    
    
def create_conclusion(service):
    #find insights & conclusions for the selected service call text function and 
    #in accordeon item.
    
    match(service):
        case 'All':
            return edt.insights_All()
        case 'Subways':
            return edt.insights_subways()
        case 'Buses':
            return edt.insights_buses()
        case 'LIRR':
            return edt.insights_LIRR()
        case 'Metro_North':
            return edt.insights_MNR()
        case 'Access_A_Ride':
            return edt.insights_AAR()
        case 'Bridges_and_Tunnels':
            return edt.insights_BAT()
        case 'Staten_Island_Railway':
            return edt.insights_SIR()
        case _:
            return edt.insights_dummy()
    
     


    

    

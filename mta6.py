# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:39:52 2024

@author: win11
"""

from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
import pandas as pd
# adds  templates to plotly.io
load_figure_template(["yeti_dark", "yeti_dark"])


# =============================================================================
# import sys
# import os
# def resource_path(relative_path):
# 
# # get absolute path to resource
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
# 
#     return os.path.join(base_path, relative_path)
# =============================================================================


#import assets.ed_data as edd

import assets.ed_functions as edf
import assets.ed_text as edt
#import assets.ed_lr as elr


#df_services, df_ridership_yw, df_ridership_yw_weekdays, df_ridership_yw_weekend = edd.data_elt()

#for the app etl is skipped in favor of importing the prepared data directly.
#only adjustment is converting dates after import.
#on github is all the dataprocessing available in ed_data.py

df_services= pd.read_csv('services_new.csv')
df_ridership_yw = pd.read_csv('ridership_yw.csv')
df_ridership_yw_weekdays = pd.read_csv('ridership_yw_weekdays.csv')
df_ridership_yw_weekend = pd.read_csv('ridership_yw_weekend.csv')

df_ridership_yw['Date'] = pd.to_datetime(df_ridership_yw['Date']) 
df_ridership_yw_weekdays['Date'] = pd.to_datetime(df_ridership_yw_weekdays['Date']) 
df_ridership_yw_weekend['Date'] = pd.to_datetime(df_ridership_yw_weekend['Date']) 








def display_totals(df_in,service,df_services,view,title):
    
    #the correct column to use is decided by the selected service
    #columnnames have the servicename as prefix except in services
    
    prepan = service+"_sum_tot_prepan"
    postpan = service + "_sum_tot_postpan"
    y_max = df_services[df_services['Service']==service]['sum_max_value'].values[0]
    
    
    fig=go.Figure()
    
    
    
    
    fig.add_trace(go.Scatter(x=df_in['Date'], y=df_in[prepan], fill='tozeroy',name="Pre-pandamic     *"
                           ,connectgaps=True  ))
    fig.add_trace(go.Scatter(x=df_in['Date'], y=df_in[postpan], fill='tozeroy', 
                       line_color='rgba(255, 215, 0,.6)',fillcolor='rgba(0, 140, 186,.7)',name="Post-pandemic",connectgaps=True))
    
    
    
    
    
    fig.update_layout(

        title=dict(
    text=title,
    font_size=18,
    automargin=True,
    yref='container'
),
        legend=dict(
            orientation="h",
            traceorder="reversed",
            yanchor="bottom",
            y=1.10,
            xanchor="right",
            x=1
            )
    ),
    
    #yaxes max value is set per service
    fig.update_yaxes(range=[0, y_max], fixedrange=True)
    fig.update_xaxes(title="Timeline",

                     #fixedrange=True
                     ),
    

         

    #linear regression, y=ax + b, if you draw a staight line, it's
    #enough to have the start and endpoint.{trend} =  columnname for selected service 
    
    #index_start = df_in.query(f"{trend} > 0").index[0]
    #index_end = len(df_in) - 1
    
    xstart, ystart = edf.get_first_trendline_xy(df_in, service)
    xend, yend = edf.get_last_trendline_xy(df_in, service)
       

         
    fig.add_shape(type="line",
     x0=xstart, y0=ystart, x1=xend, y1=yend,
     showlegend = True,
     name="Post-pandemic trend",
     line=dict(
         color="#FFD700",
         width=3,
         dash="dot",
         
     ),
 )
         
         
         

    
    return fig

def display_percentages(df_in,service,df_services,view,title):
    

    perc = service+"_perc_postpan_as_prepan"
    y_max = 140


    #horizontal green 100%
    
    fig=go.Figure()
    fig.update_layout(shapes=[
    dict(
      type= 'line',
      yref= 'y', y0= 100, y1= 100,
      xref= 'paper', x0= 0, x1= 1,
      showlegend = True,
      name="100%: recovery",
      line=dict(
                    color="#70d158",
                    width=1,
                    dash="dot",
                )
    ),
    #horizontal orange #f2850d
    dict(
      type= 'line',
      yref= 'y', y0= 80, y1= 80,
      xref= 'paper', x0= 0, x1= 1,
      showlegend = True,
      name="80%: recovery",
      line=dict(
                    color="#f2850d",
                    width=1,
                    dash="dot",
                )
    )
    
    
    ]),
    
    
    

                    
 

    fig.add_trace(go.Scatter(x=df_in['Date'], y=df_in[perc], fill='tozeroy', 
                       line_color='#FFD700',fillcolor='rgba(0, 140, 186,.7)',
                       name="Percentage recovered",xperiodalignment="end",connectgaps=True, 
                       showlegend = False
                       ))
    fig.update_layout(
            title=dict(
            text=title,
            font_size=18,
            automargin=True,
            yref='container'
            ),
        legend=dict(
            orientation="h",
            traceorder="reversed",
            yanchor="bottom",
            y=1.10,
            xanchor="right",
            x=1
            )
    ),
    #yaxes max value is set per service
    fig.update_yaxes(range=[0, y_max], #fixedrange=True,
                     
                     tickvals = [0,20,40,60,80,100,120,140],
                     ticktext = ['0%','20%','40%','60%','80%','100%','120%','140%'], 
                     
                     
                     )
    fig.update_xaxes(title="Timeline",

                     fixedrange=True
                     ),
     

    
    return fig




app = Dash(__name__, external_stylesheets=[dbc.themes.YETI, dbc.icons.FONT_AWESOME])




app.layout = dbc.Container(
    [   
        html.Div(["MTA services: dive into post-pandemic recovery trends by week"], className="text-white h1 p-2", id = "Top"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Row([

                       html.Div([
                           #no mobile first behaviour?
                           
                           dcc.Dropdown(
                               id='select_view',
                               options=[{'label': 'Show recovery in %', 'value': 'vperc'},
                                        {'label': 'Show trendline in #', 'value': 'vsum'}
                                        ],
                               value='vperc',clearable = False, searchable = False, style={'backgroundColor':'#383838', 'color':'white'}
               ),
                           ], className = "col-lg-6"),
                        html.Div([
                            dcc.Dropdown(
                                id='select_service',
                                options=edf.create_services_options(df_services),
                                value='All' ,clearable = False, searchable = False, style={'backgroundColor':'#383838', 'color':'white'}
                ),
                            ],  className = "col-lg-6"),



                       ],  style={'marginBottom':'2rem', 'padding':'2rem'}),



                   
                    
               html.Div([
                    
                        
                        dbc.Tabs([
                            dbc.Tab(tab_id = 'ridership-graph', label='Ridership trend'),
                            dbc.Tab(tab_id = 'weekdays-graph', label='Only weekdays'),
                            dbc.Tab(tab_id = 'weekend-graph', label='Only weekends'),
                            ], id="tabs-example-graph", active_tab='ridership-graph'),
                        html.Div(id='tabs-content-example-graph')
                        
                        
                        ])
                    
                    
                    ],  style={'backgroundColor': '#222','marginBottom':'2rem'})
                   
                    
                
                
            
            ], className = "col-lg-8"),
            
            dbc.Col([
                
                
                html.Div(id="card_perfomance_past"),
                html.Div(id="card_perfomance_expectations"),
                
                
                dbc.Accordion([
   
                dbc.AccordionItem(
                [
                    html.Div(id="conclusions_info_output"),
                ],
                title="Insights & suggestions",  item_id="conclusions"
                ),
                dbc.AccordionItem(
                [
                    html.Div(id="general_info_output"),
                ],
                title="More about this service", item_id="general_info"
                ),
                dbc.AccordionItem(
                    html.Div(id="data_info_output"),
                title="How was data collected?", item_id="data_info"
                ),
                ], id="accordion",
                 active_item="conclusions"),
                html.Div(id="accordion-contents", className="mt-3"),
    
                
                ],  className = "col-lg-4")
            
            
            
            ],className = ""),

            
            dbc.Button("Go Home!", href="#top", id="button", className = "fixed-button"),    
               

       
    ], style={'backgroundColor': '#333', 'marginTop': '2rem'}
 
)



# FILTERING & UPDATING VISUALS #




@app.callback( Output('tabs-content-example-graph', 'children'),

          [Input('tabs-example-graph', 'active_tab'),
          Input(component_id='select_service', component_property='value'),
          Input(component_id='select_view', component_property='value')]

          
          )

def render_content(tab,service,view):
     #probaly the best place to create the plottitle because tabselection is 
     #known and should be included in the title.
     
     
     
     title = ""
     if tab == 'ridership-graph' and view == 'vsum':
        title = service.replace('_', ' ') + ": Ridership in numbers comparing pre-vs post-pandemic"
        visual = html.Div([
            dcc.Graph(figure=display_totals(df_ridership_yw,service,df_services,view,title)),
            edt.show_explanation_totals()
           
         ]),

     elif tab == 'weekdays-graph'  and view == 'vsum':
        title = service.replace('_', ' ') + ": Ridership in numbers comparing pre- vs post-pandemic (weekdays)"
        visual = html.Div([
            dcc.Graph(figure=display_totals(df_ridership_yw_weekdays,service,df_services,view,title)),
            edt.show_explanation_totals()
         ]),

     elif tab == 'weekend-graph'  and view == 'vsum':
        title = service.replace('_', ' ') + ": Ridership in numbers comparing pre-p vs post-pandemic (weekends)" 
        visual =html.Div([
            dcc.Graph(figure=display_totals(df_ridership_yw_weekend,service,df_services,view,title)),
            edt.show_explanation_totals()
         ]),

     elif tab == 'ridership-graph' and view == 'vperc':
        title = service.replace('_', ' ') + ": Post-pandemic ridership as % of pre-pandemic estimate" 
        visual = html.Div([
            dcc.Graph(figure=display_percentages(df_ridership_yw,service,df_services,view,title)),
            edt.show_explanation_percentages()
           
         ]),

     elif tab == 'weekdays-graph'  and view == 'vperc':
        title = service.replace('_', ' ') + ": Post-pandemic ridership as % of pre-pandemic estimate (weekdays)" 
        visual =html.Div([
            dcc.Graph(figure=display_percentages(df_ridership_yw_weekdays,service,df_services,view,title)),
            edt.show_explanation_percentages()
         ]),

     elif tab == 'weekend-graph'  and view == 'vperc':
        title = service.replace('_', ' ') + ": Post-pandemic ridership as % of pre-pandemic estimate (weekends)" 
        visual =html.Div([
            dcc.Graph(figure=display_percentages(df_ridership_yw_weekend,service,df_services,view,title)),
            edt.show_explanation_percentages()
         ]),

    
     return visual
 
    
 
    
 
    
@app.callback( Output('card_perfomance_past', 'children'),
          Input(component_id='select_service', component_property='value'),
          Input(component_id='select_view', component_property='value'))


def update_card_performance_past(service,view):
    
    
    card = edf.update_card_performance_past(service, df_services, view)
       
    
    return card


@app.callback( Output('card_perfomance_expectations', 'children'),
          Input(component_id='select_service', component_property='value'),
          Input(component_id='select_view', component_property='value'))


def update_card_performance_expectations(service,view):
    
    
    
    card = edf.update_card_performance_expectations(service,df_services,df_ridership_yw, df_ridership_yw_weekdays, df_ridership_yw_weekend, view)
       
    
    return card


 

##UPDATING accordionINFO ##

@app.callback(
    Output("conclusions_info_output", "children"),
    Output("general_info_output", "children"),
    Output("data_info_output", "children"),
    [Input("accordion", "active_item"),
     Input(component_id='select_service', component_property='value'),]
)
def update_accordion_item(item,service):
    
    output_conclusions_info =  edf.create_conclusion(service)
    output_general_info =  edf.create_general_information_card(service,df_services)
    output_data_info = edf.create_data_information_card(service,df_services)

    
    return output_conclusions_info, output_general_info, output_data_info


#scroll to top, not really :-)

app.clientside_callback(
    """function (id) {
        var myID = document.getElementById(id)
    
        var myScrollFunc = function() {
          var y = window.scrollY;
          if (y >= 400) {
            myID.style.display = ""
          } else {
            myID.style.display = "none"
          }
        };
        
        window.addEventListener("scroll", myScrollFunc);
        return window.dash_clientside.no_update
    }""",
    Output('button', 'id'),
    Input('button', 'id')
)





if __name__ == "__main__":
    app.run_server(debug=True)
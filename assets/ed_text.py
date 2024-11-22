# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 13:36:11 2024

@author: win11
"""
from dash import  html
import dash_bootstrap_components as dbc
import assets.ed_style as eds

def show_explanation_percentages():
    explanation = "* This visual shows actual ridership as a percentage of pre-pandemic ridership. \
        Numbers are calculated week over week and based on estimates over the last 4.5 years."

    return html.Div([
        html.P(explanation)
        ],className = "font-small padding-lr-1rem")

def show_explanation_totals():
    explanation = "* this visual shows actual ridership versus pre-pandemic ridership in absolute numbers. \
        Numbers are calculated week over week and based on estimates over the last 4.5 years. The trendline \
            is based on linear regression over the last 3 years (156 weeks). This means the trendline shows \
                the trend of increase/decrease over the last 3 years. Totals in 1 and 2 years are equal to \
                extending this trendline and calculate what the actual weekly ridership in 1 and 2 years could be."

    return html.Div([
        html.P(explanation)
        ],className = "font-small padding-lr-1rem")

def total_trendline_paragraph():
    
    text = "Based on the trend for the last 3 years a prediction can be done for weekly numbers in 1 and 2 years.\
        This prediction does not take into regard influences like changing customer behaviour, another pandemic and marketing."
        
    return html.P(text)

def perc_explanation_icons():
    
    images = {'r': 'assets/no.svg', 'o' : 'assets/maybe.svg', 'g': 'assets/yes.svg' }
    alttext = {'r': 'not recovered', 'o' : '80% recovered', 'g': '100% recovered' }
    text_red = " less recovery"
    text_green = " 100% recovery"
    text_orange = " 80% recovery"
    
 
    
    explanation = html.Div([
        html.P("Explanation: last year at least 26 or more weeks showed:", className = "font-small"),
        dbc.ListGroup(
                [
                    dbc.ListGroupItem([html.Img(src=images.get('g'), alt = alttext.get('g'),  className="arrow-sm"),html.Span(text_green,className = "font-small")]),
                    dbc.ListGroupItem([html.Img(src=images.get('o'), alt = alttext.get('o'),className="arrow-sm"),html.Span(text_orange,className = "font-small")]),
                    dbc.ListGroupItem([html.Img(src=images.get('r'), alt = alttext.get('r'),className="arrow-sm"),html.Span(text_red,className = "font-small")]),
                ],
                horizontal=True,
                flush=True,
            )
        
        ])
    
    return explanation



def numbers_explanation_cubes():
    
    text_green = 'Yes, above 100%'
    text_red = 'Less than 80%'
    text_orange = 'Above 80%'
    
 
    
    explanation = html.Div([
        html.P("Does the predicted value in 1 or 2 years exceed the average pre-pandemic value of last year?"),
        dbc.ListGroup(
                [
                    dbc.ListGroupItem([html.Span(style=eds.cube_green()),html.Span(text_green,className = "font-small")]),
                    dbc.ListGroupItem([html.Span(style=eds.cube_orange()),html.Span(text_orange,className = "font-small")]),
                    dbc.ListGroupItem([html.Span(style=eds.cube_red()),html.Span(text_red,className = "font-small")]),
                ],
                horizontal=True,
                flush=True,
            )
        
        ])
    
    return explanation






def insights_subways():
    
    #checked
    
    insights_subways = html.Div(
        [
            html.H4('Insights'),
            html.P('Subway travel has not yet recovered, primarily due to a decline in weekday ridership.'),
            html.P('It is expected that weekday recovery may take several years, whereas weekend travel could return to pre-pandemic levels faster.'),
            html.H4('Suggestions'),
            html.P('Investigate the causes: Have passengers not returned due to the rise of remote work? Has subway travel become less appealing for other reasons'),
            html.P('Focus on marketing efforts specifically aimed at attracting weekday commuters.'),
            
            ])
   
    
    return insights_subways


def insights_buses():
    #checked
    
    insights_buses = html.Div(
        [
            html.H4('Insights'),
            html.P('Bus travel has yet to recover to even 80% of pre-pandemic levels, meaning millions of people now use buses less frequently or not at all.'),
            html.P('The outlook is not encouraging unless action is taken. At best, weekday ridership may hold steady, while weekends might see only a slight increase.'),
            html.P('The way data was collected and pre-pandemic was estimated, suggests that pre-pandemic estimations could be too optimistic or post-pandemic ridership too pessimistic.', className="font-small"),
           
            html.H4('Suggestions'),
            html.P('Investigate the causes: Could it be that people simply forgot about the bus? Bus travel took the longest to begin recovering after the lockdowns. Many may have turned to alternatives during that time and stuck with them, never reconsidering the bus as an option.'),
            html.P('Do people feel less safe on buses? Are they being cleaned less frequently? It\'s crucial to understand why bus travel has declined so significantly and why ridership has not returned to pre-pandemic levels.'),
            html.P('Once the reasons are clearer, address the issues and invest in targeted marketing efforts that highlight improvements in these areas.'),
            
            ])
   
    
    return insights_buses





def insights_LIRR():
    #checked
    
    insights_LIRR = html.Div(
        [
            html.H4('Insights'),
            html.P('While weekend ridership on the Long Island Rail Road has surpassed pre-pandemic levels, weekday ridership remains below 80% of its pre-pandemic figures.'),
            html.P('However, if the current recovery trend continues, weekday ridership could eventually return to pre-pandemic levels as well.'),
            html.H4('Suggestions'),
            html.P('Investigate the causes: In addition to the impact of remote work, it would be valuable to analyze the various branches of the LIRR to determine if recovery rates differ between them during the week or if the slower recovery is a consistent pattern across all branches.'),
            #html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    
    return insights_LIRR



def insights_MNR():
    #checked
    
    insights_MNR = html.Div(
        [
            html.H4('Insights'),
            html.P('While weekend ridership on the Metro North Rail Road has surpassed pre-pandemic levels, weekday ridership remains below 80% of its pre-pandemic figures.'),
            html.P('However, if the current recovery trend continues, weekday ridership could eventually return to pre-pandemic levels as well.'),
            html.P('If this sounds familiar, yes, Metro-North and the Long Island Rail Road follow almost the same recovery pattern.'),
 
            html.H4('Suggestions'),
            html.P('Investigate the causes: In addition to the impact of remote work, it would be valuable to analyze the various branches of the MNR to determine if recovery rates differ between them during the week or if the slower recovery is a consistent pattern across all branches.'),
            #html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    
    return insights_MNR


def insights_AAR():
    #checked
    
    insights_AAR = html.Div(
        [
            html.H4('Insights'),
            html.P('Access-A-Ride experienced a rapid recovery following the lockdown and has now fully returned to pre-pandemic levels. '),
            html.P('If the current trend continues, Access-A-Ride ridership may even surpass pre-pandemic levels significantly. This actually happens already.'),

 
            html.H4('Suggestions'),
            html.P('If this growth is beneficial, no action may be needed. However, if increased ridership poses challenges, it might be time to investigate whether the criteria for "eligible customers" have shifted during the pandemic. '),
            #html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    
    return insights_AAR

def insights_SIR():
    #checked
    
    insights_SIR = html.Div(
        [
            html.H4('Insights'),
            html.P('The Staten Island Railway has not returned to its pre-pandemic ridership levels.'),
            html.P('Without intervention, there is little indication that it will recover within the next two years.'),

 
            html.H4('Suggestions'),
            html.P('Survey Commuters: Understand why former riders haven’t returned—whether it’s due to work habits, convenience, or safety concerns.'),
            html.P('Analyze Alternatives: Look at competing transit options, like express buses and ferries, to determine if they’re drawing riders away.'),
            html.P('Review Service Levels: Ensure the SIR offers competitive and attractive service, especially during peak hours.'),
            html.P('Did research this a bit, but chatgtp describes it much nicer.', className = "font-small")
            

            
            
            #html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    return insights_SIR


def insights_BAT():
    #checked
    
    insights_BAT = html.Div(
        [
            html.H4('Insights'),
            html.P('The Bridges & Tunnels service was the quickest to fully recover following the lockdown.'),
            html.P('Current ridership slowly increases above pre-pandemic levels.'),

 
            html.H4('Suggestions'),
            html.P('Maintain the current service level.'),
            #html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    return insights_BAT



def insights_All():
    #checked
    
    insights_All = html.Div(
        [
            html.H4('Insights'),
            html.P('Subways and buses together account for approximately 75% of total ridership, but both still struggle to recover.'),
            html.P('The subway is expected to reach 80% of its pre-pandemic ridership within two years, while bus ridership is unlikely to recover to that extent.'),
            html.P('Meanwhile, Bridges & Tunnels and Access-A-Ride services have fully recovered or even surpassed pre-pandemic levels.'),
            html.P('Metro-North and the Long Island Rail Road are still in recovery but show an upward trend.'),
            html.P('In contrast, the Staten Island Railway has not regained its pre-pandemic ridership, with no signs of improvement coming up.'),


 
            html.H4('Suggestions'),
            html.P('Select a service to see insights and suggestions by service.'),
            #html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    return insights_All



def insights_dummy():
    
    insights_dummy = html.Div(
        [
            html.H4('Dummy Insights'),
            html.P('Travelling by Subway has not recovered, mostly due to a lack of passengers during weekdays.'),
            html.P('The expectation is that weekday recovery will take many years while weekend travel could recover in 2 years.'),
            html.H4('Suggestions'),
            html.P('Investigate causes: returning customers working from home, travelling by subway is not attractive (anymore) etc. '),
            html.P('Invest in marketing targeted at weekday travellers.'),
            
            ])
   
    
    return insights_dummy
    
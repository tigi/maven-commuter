# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:03:44 2024

@author: win11
"""

#getting tired of yes/no picking up css and in which order
#cubes are for explaining assigned colors in numberanalysis
def cube_red():
    
    layout_style={'height': '10px',
                  'width' : '10px',
                  'paddingRight':'10px',

                  'marginRight':'.5rem',
                  'backgroundColor': '#e33636'}
    
    
    return layout_style

def cube_orange():
    
    layout_style={'height': '10px',
                  'width' : '10px',
                  'paddingRight':'10px',
                  'marginRight':'.5rem',
                  'backgroundColor': '#f2870c'}
    
    
    return layout_style

def cube_green():
    
    layout_style={'height': '10px',
                  'width' : '10px',
                  'paddingRight':'10px',
                  'marginRight':'.5rem',
                  'backgroundColor': '#70d158'}
    
    
    return layout_style



#UI should be separate .py, some generic functions and styledefinitions, somehow /assets/custom.css
#stopped loading, this is faster than solving the local problem



def style_h2():
    layout_style={'fontSize': '1.5rem',
                  'marginBottom':'1.8rem',
                  }
    return layout_style

def style_h3():
    layout_style={'fontSize': '1.2rem',
                  'marginBottom':'1.5rem',
                  }
    return layout_style



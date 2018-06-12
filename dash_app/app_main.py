import dash
from dash.dependencies import Input, Output
import dash_html_components as dhc
import dash_core_components as dcc
import plotly.offline as py
import pandas as pd
import numpy as np
#from itertools import izip
from plotly.widgets import GraphWidget
#from datetime import datetime, timedelta
from pandas.api.types import is_string_dtype
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets
from plotly import tools
from pandas.io import gbq
from config import df, pcd, sasby, avg_user, avg_attempted, avg_incorrect, avg_partially_correct, avg_correct, avg_sa_correct, avg_pct_sa_partially_correct, avg_pct_sa_correct, avg_pct_sa_incorrect, user_dict, total, date_init, date_last, all_users, total_days, STARTING_USER, df_col_list2, max_attempt

from utils import scatter_plot_2d, horizontal_barchart, barchart, update
import flask
from flask import url_for, redirect
import plotly
import plotly.graph_objs as go

from app import app


BACKGROUND = 'rgb(230, 230, 230)'


COLORSCALE = [ [0, "rgb(244,236,21)"], [0.3, "rgb(249,210,41)"], [0.4, "rgb(134,191,118)"], 
                [0.5, "rgb(37,180,167)"], [0.65, "rgb(17,123,215)"], [1, "rgb(157, 48, 165)"] ]

layout = dhc.Div([
    dhc.Link(
        rel="stylesheet",
        href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    ),     
    dhc.Link(
        rel="stylesheet",
        href="//fonts.googleapis.com/css?family=Raleway:400,300,600"
    ),

    # Row 1: Header and Intro text
        
    dhc.Div([
                
        dhc.Div([
            dhc.H2('edX data analysis demo'),
            dhc.P('Each point in the scatter plot below represents an enrolled user. SELECT a user in the dropdown menu or from the graph.'),                        
            ], className="col-md-6" ),
        
        dhc.Div([
            dhc.Br(),
            dcc.Dropdown(id='user_dropdown', 
                        multi=False,
                        value=STARTING_USER,
                        options=[{'label': i, 'value': i} for i in df['user_id'].tolist()]),
            ], className="col-md-6" ),
        
    ], className='container' ),


    # Row 2: Hover Panel and Graph
      
    dhc.Div([
        dhc.Hr(),
        dhc.Div([ 
            dcc.Tabs(
                tabs=[
                    {'label': 'Absolute values', 'value': 1},
                    {'label': 'Percentile ranks', 'value': 2},
                ],
                value=1,
                id='tabs',
                #vertical=vertical
            ),            
            dcc.Graph(id='clickable-graph', 
                      style=dict(height='500px'),
                      clickData=dict( points=[dict(pointNumber=0)] )
                     ),                                            
            dhc.Div([  
                dhc.Br(),
                dhc.Div([ 
                    dhc.B('X axis:'),
                    dhc.Br(),
                    dcc.Dropdown(
                        id='crossfilter-xaxis-column',
                        options=[{'label': i, 'value': i} for i in df_col_list2 ],
                        value='nshow_answer'
                    ),
                    dcc.RadioItems(
                        id='crossfilter-xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                        value='linear',
                        labelStyle={'display': 'inline-block'}
                    ),
                ], className='col-md-3'),                
                dhc.Div([             
                #dhc.Br(),
                #html.Br(),    
                dhc.B('Y axis:'),
                dhc.Br(),            
                dcc.Dropdown(
                    id='crossfilter-yaxis-column',
                    options=[{'label': i, 'value': i} for i in df_col_list2 ],
                    value='nvideo'
                ),
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                    value='linear',
                    labelStyle={'display': 'inline-block'}
                ),
                ], className='col-md-3'),                 
            ], className='container'),             
                        
        ], className='col-md-7'),
        
        dhc.Div([ 

            dcc.Graph(id='horizontal_barchart_graph', 
                      style=dict(height='300px'),
                      #figure=SIDE_PLOT 
                     ),            
            
            #dcc.Graph(id='donut-graph', 
            #          style=dict(height='300px'),
            #          #figure=SIDE_PLOT 
            #         ),
            
            dcc.Graph(id='bar-chart',
                     style=dict(height='300px'),
                     #figure=BAR_CHART
                     ),
            
            
            dhc.P('The darker-colored bars represent the individual user - the lighter-colored ones represent the average.'),
            
        ], className="col-md-5") 
                
    ], className='container'),

    
    dhc.Div([
        dhc.Hr(),
        dcc.Graph(id='timeseries-graph', 
                  #figure=TIMESERIES 
                 )
    ])
            
], className = 'container')


@app.callback( 
    Output('user_dropdown', 'value'),
    [Input('clickable-graph', 'clickData')])
def return_user( clickData ):
    print '\n\n clickdata: ',clickData
    if clickData is not None:
        if 'points' in clickData:    
            firstPoint = clickData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                print 'point_number',point_number
                if point_number == 0:
                    user_name = STARTING_USER
                else:
                    print 'username directly from clickData', clickData['points'][0]['text']
                    user_name = int(clickData['points'][0]['text'])
                return user_name


@app.callback( 
    Output('clickable-graph', 'figure'),
    [Input('user_dropdown', 'value'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-column', 'value'),     
    Input('crossfilter-yaxis-type', 'value'),   
    Input('tabs', 'value'),
    ])
def highlight_user( user_dropdown_value, xaxis_col, xaxis_type, yaxis_col, yaxis_type,tab_output ):
    #print 'flask session:',flask.session
    #print 'flask session:',flask.session['check']    
    #print 'dataset_type:',flask.session['dataset_type']
    print 'user_dropdown_value',user_dropdown_value
    scatter_plot = scatter_plot_2d(user_dropdown_value, xaxis_col, xaxis_type, yaxis_col, yaxis_type,tab_output )
    return scatter_plot

@app.callback( 
    Output('horizontal_barchart_graph', 'figure'),
    [Input('user_dropdown', 'value')])
def user_horizontal_barchart( user_dropdown_value ):
    print 'user_dropdown_value',user_dropdown_value
    hor_barchart = horizontal_barchart( user_dropdown_value )
    return hor_barchart
"""
@app.callback( 
    Output('donut-graph', 'figure'),
    [Input('user_dropdown', 'value')])
def user_donuts( user_dropdown_value ):
    print 'user_dropdown_value',user_dropdown_value
    donut = simple_donut( user_dropdown_value )
    return donut
"""


@app.callback( 
    Output('bar-chart', 'figure'),
    [Input('user_dropdown', 'value')])
def user_bar( user_dropdown_value ):
    bar = barchart( user_dropdown_value )
    return bar


@app.callback(
    Output('timeseries-graph', 'figure'),
    [Input('user_dropdown', 'value')])
def timeseries( user_dropdown_value ):
    timechart = update( user_dropdown_value )
    return timechart 

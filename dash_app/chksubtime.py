import base64
import io

import dash
import json
from datetime import datetime, tzinfo #as dt
import dateutil.parser as du
import pytz
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt

import pandas as pd
from utils import datetime_to_json, get_datetime

from app import app

est = pytz.timezone('US/Eastern')
layout = html.Div([
    html.H3("Check submission time of answer strings from MITx"),
    html.Br(),
    
    html.H4("STEP 1: Upload the response file :"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload File',className="btn btn-md btn-default"),
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='data-dump', style={'display': 'none'}),
    html.Div(id='date-time-dump', style={'display': 'none'}),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    html.Hr(),
    html.Div(id='dd-datetimepicker',children=[
            html.Div([
                    html.H4("STEP 2: Choose the date-time range to process the uploaded file"),
                    html.P("All times are in US/Eastern timezone"),
                    html.Hr(),
                    html.Div([
                        html.H5("Start date-time:"),
                        html.Div([

                                html.B('Date (MM/DD/YYYY)'),
                                html.Br(),
                                dcc.DatePickerSingle(
                                    id='start-date',
                                    min_date_allowed=datetime(2014, 8, 5),
                                    max_date_allowed=datetime(2024, 9, 19),
                                    #initial_visible_month=start_date,
                                    #date=start_date
                                ),],className="col-md-4"),
                        html.Div([
                                html.B("hh "),
                                dcc.Dropdown(
                                    id='start-time-hh',
                                    options=[{'label': '{:02d}'.format(hh), 'value': hh} for hh in range (0,24)],
                                    #value=min(ts_list).hour,
                                    clearable=False
                                ),],className="offset-col-md-2 col-md-2"),
                        html.Div([   
                                html.B("mm "),                            
                                dcc.Dropdown(
                                    id='start-time-mm',
                                    options=[{'label': '{:02d}'.format(mm), 'value': mm} for mm in range (0,60)],
                                    #value=min(ts_list).minute,
                                    clearable=False
                                ),],className="col-md-2"),
                        html.Div([
                                html.B("ss "),                            
                                dcc.Dropdown(
                                    id='start-time-ss',
                                    options=[{'label': '{:02d}'.format(ss), 'value': ss} for ss in range (0,60)],
                                    #value=min(ts_list).second,
                                    clearable=False
                                ),],className="col-md-2"),   
                    ],className="col-md-6"),  
                    html.Div([
                        html.H5("End date-time:"),
                        html.Div([
                                html.B('Date (MM/DD/YYYY)'),
                                html.Br(),
                                dcc.DatePickerSingle(
                                    id='end-date',
                                    min_date_allowed=datetime(2014, 8, 5),
                                    max_date_allowed=datetime(2024, 9, 19),
                                    #initial_visible_month=end_date,
                                    #date=end_date
                                ),],className="col-md-4"),
                        html.Div([
                                html.B("hh "),
                                dcc.Dropdown(
                                    id='end-time-hh',
                                    options=[{'label': '{:02d}'.format(hh), 'value': hh} for hh in range (0,24)],
                                    #value=max(ts_list).hour,
                                    clearable=False
                                ),],className="offset-col-md-2 col-md-2"),
                        html.Div([   
                                html.B("mm "),                            
                                dcc.Dropdown(
                                    id='end-time-mm',
                                    options=[{'label': '{:02d}'.format(mm), 'value': mm} for mm in range (0,60)],
                                    #value=max(ts_list).minute,
                                    clearable=False
                                ),],className="col-md-2"),
                        html.Div([
                                html.B("ss "),                            
                                dcc.Dropdown(
                                    id='end-time-ss',
                                    options=[{'label': '{:02d}'.format(ss), 'value': ss} for ss in range (0,60)],
                                    #value=max(ts_list).second,
                                    clearable=False
                                ),],className="col-md-2"),   
                    ],className="col-md-6"),
                
                    html.Br(),

                    ]),
    ]),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Div(id='filtered-df'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.P('Questions/comments/bugs? Email anindyar@mit.edu'),
    html.A("Github repo",
          href="https://github.com/royanin/edx2bq_analysis_demo",
          target="_blank"),
], className='container' )


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        #df.to_csv('data/uploaded_file.csv',index=False)
        
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
        
    datasets = {
         'df_sel': df.to_json(orient='split', date_format='iso')
    }

    return json.dumps(datasets)

@app.callback(Output('data-dump', 'children'),
    #Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
Output('output-data-upload', 'children'),
[Input('data-dump', 'children'),
])
def show_df(json_dataset):
    #print json_dataset[0]
    if json_dataset is None:
        pass
        #return html.Div("Sorry -- can\'t show the file",
        #              style={'text-align':'center'})
    else:
        datasets = json.loads(json_dataset[0])
        df = pd.read_json(datasets['df_sel'], orient='split')

    return html.Div([
        #html.H5(filename),
        #html.H6(datetime.datetime.fromtimestamp(date)),

        # Use the DataTable prototype component:
        # github.com/plotly/dash-table-experiments
        dt.DataTable(rows=df.to_dict('records')),

        html.Hr(),  # horizontal line
        #html.Div(col_string)
        
    ])

@app.callback(
Output('filtered-df', 'children'),
[Input('data-dump', 'children'),
 Input('start-date', 'date'),
 Input('end-date', 'date'),
 Input('start-time-hh', 'value'),
 Input('start-time-mm', 'value'),
 Input('start-time-ss', 'value'), 
 Input('end-time-hh', 'value'),
 Input('end-time-mm', 'value'),
 Input('end-time-ss', 'value'),  
])
def show_filtered_df(json_dataset, start_date, end_date, start_hh, start_mm, start_ss, end_hh, end_mm, end_ss):

    #print "In show_filtered_df", start_date, end_date,  start_hh, start_mm, start_ss, end_hh, end_mm, end_ss
    fmt = '%Y-%m-%d %H:%M:%S'

    start_dt = get_datetime(start_date,start_hh, start_mm, start_ss,est)
    end_dt = get_datetime(end_date,end_hh, end_mm, end_ss,est)
    #print 'start_dt/end_dt',start_dt, end_dt
    if json_dataset is None:

        return html.Div("", style={'text-align':'center'})
    else:
        datasets = json.loads(json_dataset[0])
        df = pd.read_json(datasets['df_sel'], orient='split')
        
    if df is not None:
        if start_dt > end_dt:
            return html.Div([
                html.H5("Invalid time range"),
                html.P("Start time is after the end time"),
            ])
        col_string = ", ".join(df.columns.tolist())
        flat_list = []
        flat_list_before = []
        flat_list_after = []
        flat_list_during = []        
        for i in range (0,df.shape[0]):
            a = json.loads(df.iloc[i][1])
            try:
                print_t = du.parse(a['last_submission_time']).astimezone(est).strftime(fmt)
                if du.parse(a['last_submission_time'])> end_dt:
                    flat_list_after.append({'username':df.iloc[i][0],
                                     'last_submission_time':print_t
                                           })
                elif du.parse(a['last_submission_time'])< start_dt:
                    flat_list_before.append({'username':df.iloc[i][0],
                                     'last_submission_time':print_t
                                            })
                elif ((du.parse(a['last_submission_time'])>= start_dt ) 
                      and (du.parse(a['last_submission_time'])<= end_dt)):
                    flat_list_during.append({'username':df.iloc[i][0],
                                     'last_submission_time':print_t
                                            })
            except KeyError:
                pass
            

        ret_list = [html.Br()]
        if len(flat_list_after)>0:
            flat_df_after = pd.DataFrame(flat_list_after)
            ret_list.append(html.H5("{} response(s) received after the specified time range".format(len(flat_list_after)))),
            ret_list.append(dt.DataTable(rows=flat_df_after.to_dict('records')))
            ret_list.append(html.Br())
        if len(flat_list_before)>0:
            flat_df_before = pd.DataFrame(flat_list_before)
            ret_list.append(html.H5("{} response(s) received before the specified time range".format(len(flat_list_before)))),            
            ret_list.append(dt.DataTable(rows=flat_df_before.to_dict('records')))
            ret_list.append(html.Br())            
        if len(flat_list_during)>0:
            ret_list.append(html.H5("{} response(s) received during the specified time range".format(len(flat_list_during)))),            
            flat_df_during = pd.DataFrame(flat_list_during)            
            ret_list.append(dt.DataTable(rows=flat_df_during.to_dict('records')))
            ret_list.append(html.Br())            
        
        return html.Div(ret_list)
        
        
    else:
        pass
        #col_string = 'Sorry, can\'t get the file names.'
  
        

@app.callback(
Output('date-time-dump', 'children'),
[Input('data-dump', 'children'),
])
def show_filtered_df(json_dataset):
    #print json_dataset[0]
    if json_dataset is None:
        pass
        #return html.Div("Sorry -- can\'t show the file",
        #               style={'text-align':'center'})
    else:
        datasets = json.loads(json_dataset[0])
        df = pd.read_json(datasets['df_sel'], orient='split')
    if df is not None:
        ts_list = []
        for i in range (0,df.shape[0]):
            a = json.loads(df.iloc[i][1])
            try:
                #q1 = a['last_submission_time']
                ts_list.append(du.parse(a['last_submission_time']))
            except KeyError:
                pass
                #print (str(i+1)+','+df.iloc[i][0]+','+q1)        
    
        if len(ts_list)>0:
            #tz=datetime.tzinfo.tzname('US/Eastern')
            #print max(ts_list).astimezone(),min(ts_list).astimezone()
            #Return the date/time selector dropdown lists
            date_time_dict = {}
            date_time_dict['start_time'] = min(ts_list).astimezone(est)
            date_time_dict['end_time'] = max(ts_list).astimezone(est)
            print date_time_dict
            return json.dumps(date_time_dict, default = datetime_to_json)
            
            #return {'display': 'visible'}
"""
OUTPUT for the date/time pickers
"""

@app.callback(
Output('start-date', 'date'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['start_time']).date()
    
@app.callback(
Output('end-date', 'date'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['end_time']).date()
    
@app.callback(
Output('start-time-hh', 'value'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['start_time']).hour
    
@app.callback(
Output('start-time-mm', 'value'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['start_time']).minute
    
@app.callback(
Output('start-time-ss', 'value'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['start_time']).second

    
@app.callback(
Output('end-time-hh', 'value'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['end_time']).hour
    
@app.callback(
Output('end-time-mm', 'value'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['end_time']).minute
    
@app.callback(
Output('end-time-ss', 'value'),
[Input('date-time-dump', 'children'),
])
def show_filtered_df(json_dt):
    if json_dt is None:
        return html.Div("")
    else:
        date_time_dict = json.loads(json_dt)
        return du.parse(date_time_dict['end_time']).second
    
    


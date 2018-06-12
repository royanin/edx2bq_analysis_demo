import pandas as pd
from config import df, pcd, sasby, avg_user, avg_attempted, avg_incorrect, avg_partially_correct, avg_correct, avg_sa_correct, avg_pct_sa_partially_correct, avg_pct_sa_correct, avg_pct_sa_incorrect, user_dict, total, date_init, date_last, all_users, total_days, STARTING_USER, df_col_list2_dict, max_attempt

import plotly
import plotly.graph_objs as go

def scatter_plot_2d(uid, xaxis_col, xaxis_type, yaxis_col, yaxis_type,tab_output ):
    if tab_output == 1:
        xcol_mod = xaxis_col
        ycol_mod = yaxis_col        
    elif tab_output == 2:
        xcol_mod = df_col_list2_dict[xaxis_col]
        ycol_mod = df_col_list2_dict[yaxis_col]
        
    traces = [go.Scatter(
            x=df[xcol_mod],
            y=df[ycol_mod],
            text = df['user_id'], 
            name='User',
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'color':'rgba(24,119,219,0.8)',
            }
        )]
    
    if uid is not None:
        print("userID: ", uid)
        row = df.loc[df['user_id']==int(uid)]
    else:
        print("No dropdown value")        
        row = df.loc[df['user_id']==STARTING_USER]        

    trace_selected = go.Scatter(
        x = [row[xcol_mod].iloc[0]],
        y = [row[ycol_mod].iloc[0]],
        text=uid,
        showlegend=False,
        name='Selected',
        mode='markers',
        marker={
            'line':{'width':3},
            'size': 15,
            'opacity': 1.0,
            'color' : 'black',
            'symbol' : 'x-open'
        }
    )
    
    traces.append(trace_selected)
    return {
        'data': traces,
        'layout': go.Layout(
            title='All Users',
            showlegend=False,
            xaxis={
                #'title': 'nshow_answer',
                'title': xcol_mod,
                'type': 'linear' if xaxis_type == 'linear' else 'log'
            },
            yaxis={
                #'title': 'nvideo',
                'title': ycol_mod,                
                'type': 'linear' if yaxis_type == 'linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 0, 'r': 0},
            hovermode='closest'
        )
    }    


def horizontal_barchart(uid):
    
    user = sasby[sasby.user_id==int(uid)]
    current_user = user.groupby('user_id').sum().reset_index()
    
    attempted = float(current_user.n_attempted)
    
    print current_user.n_attempted

    print 'in horizontal_barchart'
    incorrect = int(current_user.n_attempted[0] - current_user.n_partial[0])
    partially_correct = int(current_user.n_partial[0]  - current_user.n_perfect[0])
    correct = int(current_user.n_perfect[0])
    
    print 'incorrect, partially_correct, correct',incorrect, partially_correct, correct
    print 'figure out which is what: attempted, partial, perfect', current_user.n_attempted[0], current_user.n_partial[0], current_user.n_perfect[0]

    marker1 = dict(colors=['rgba(163, 203, 56, 1)','rgba(18, 137, 167, 1)','rgba(87, 88, 187, 1)'])    
    
    
    ylabels = ['User {}'.format(uid), 'Avg. student']
    x_incorrect = [incorrect, avg_incorrect]
    x_part_correct = [partially_correct, avg_partially_correct]
    x_correct = [correct, avg_correct]
    
    #marker_user = dict(color=['rgba(87, 88, 187, 1)','rgba(18, 137, 167, 1)','rgba(163, 203, 56, 1)'])
    #marker_avg = dict(color=['rgba(87, 88, 187, 0.5)','rgba(18, 137, 167, 0.5)','rgba(163, 203, 56, 0.5)'])    
    marker_correct = dict(color=['rgba(87, 88, 187, 1)', 'rgba(87, 88, 187, 0.5)'])
    marker_incorrect = dict(color=['rgba(163, 203, 56, 1)','rgba(163, 203, 56, 0.5)'])    
    marker_partially_correct = dict(color=['rgba(18, 137, 167, 1)','rgba(18, 137, 167, 0.5)'])
    
    
    trace_incorrect = go.Bar(
        y=ylabels,
        x=x_incorrect,
        marker=marker_incorrect,
        name='incorrect',
        orientation = 'h'
    )
    
    trace_partially_correct = go.Bar(
        y=ylabels,
        x=x_part_correct,
        marker=marker_partially_correct,
        name='partially_correct',
        orientation = 'h'
    )
    
    trace_correct = go.Bar(
        y=ylabels,
        x=x_correct,
        marker=marker_correct,
        name='correct',
        orientation = 'h'
    )    
    
    data = [trace_correct, trace_partially_correct, trace_incorrect]
    #print data
    layout = go.Layout(
    #xaxis=dict(
    #    range=[0, max_attempt]
    #),
    xaxis=dict(
        range=[0, max_attempt],
        tickfont=dict(
            size=10)),
    barmode='stack',
    title='Total number of problems attempted',
    showlegend=True)
       
    return dict(data = data, layout = layout)

def barchart(uid):
    
    user = sasby[sasby.user_id==int(uid)]
    current_user = user.groupby('user_id').sum().reset_index()
    
    attempted = float(current_user.n_attempted)
    
    print current_user.n_attempted

    incorrect = float(current_user.n_attempted) - float(current_user.n_partial)
    partially_correct = float(current_user.n_partial) - float(current_user.n_perfect)
    correct = float(current_user.n_perfect)
    
    sa_incorrect = float(current_user.n_show_answer_attempted) - float(current_user.n_show_answer_partial)
    sa_partially_correct = float(current_user.n_show_answer_partial) - float(current_user.n_show_answer_perfect)
    sa_correct = float(current_user.n_show_answer_perfect)
    
    if partially_correct > 0:
        pct_sa_partially_correct = int((sa_partially_correct / partially_correct) * 100)
    else:
        pct_sa_partially_correct = 0
    if correct > 0:
        pct_sa_correct = int((sa_correct / correct) * 100)
    else:
        pct_sa_correct = 0
    if incorrect > 0:
        pct_sa_incorrect = int((sa_incorrect / incorrect) * 100)
    else:
        pct_sa_incorrect = 0
    
 
    xlabels = ['Correct Problems', 'Partially Correct Problems', 'Incorrect Problems']
    trace1 = go.Bar(
    x=xlabels,
    y=[pct_sa_correct, pct_sa_partially_correct, pct_sa_incorrect],
    marker=dict(
        color=['rgba(87, 88, 187, 1)','rgba(18, 137, 167, 1)','rgba(163, 203, 56, 1)']),
    name='User {}'.format(uid))
    
    trace2 = go.Bar(
    x=xlabels,
    y=[avg_pct_sa_correct, avg_pct_sa_partially_correct, avg_pct_sa_incorrect],
        marker=dict(
        color=['rgba(87, 88, 187, 0.5)','rgba(18, 137, 167, 0.5)','rgba(163, 203, 56, 0.5)']),
    name='Average Student')
    
    data = [trace1, trace2]
    layout = go.Layout(
    yaxis=dict(
        range=[0,100]),
    xaxis=dict(
        tickfont=dict(
            size=10)),
    barmode='group',
    title='Percentage of Show Answer',
    showlegend=False)
       
    return dict(data = data, layout = layout)




def update(uid):
    uname = user_dict[uid][1:]
    print 'uname',uname
    user = pcd[pcd.username==uname]
    user_total = user.groupby('date').sum().reset_index()
    user_total.loc[:,('date')] = pd.to_datetime(user_total['date'])

    user_days = user_total[(user_total.date >= date_init) & (user_total.date < date_last)]
    
    trace0 = go.Scatter(x=user_days.date,
                    y=user_days.nvideo,
                    text=user_days.date,
                    marker=dict(
                        color='rgb(249,210,41)'),
                    name='videos')
    trace1 = go.Scatter(x=total_days.date,
                    y=total_days.nvideo,
                    text=total_days.date,
                    marker=dict(
                        color='rgba(249,210,41, 0.5)'),
                    line = dict(
                        width = 2,
                        dash = 'dot'),
                    name='videos average')
    trace2 = go.Scatter(x=user_days.date,
                    y=user_days.nproblems_answered,
                    text=user_days.date,
                    marker=dict(
                        color='rgb(37,180,167, 14)'),
                    name='problems')
    
    trace3 = go.Scatter(x=total_days.date,
                    y=total_days.nproblems_answered,
                    text=total_days.date,
                    marker=dict(
                        color='rgba(37,180,167, 0.5)'),
                    line = dict(
                        width = 2,
                        dash = 'dot'),
                    name='problems average')
    trace4 = go.Scatter(x=user_days.date,
                    y=user_days.nshow_answer,
                    text=user_days.date,
                    marker=dict(
                        color='rgb(54,50,153)'),
                    name='show answer')
    trace5 = go.Scatter(x=total_days.date,
                    y=total_days.nshow_answer,
                    text=total_days.date,
                    marker=dict(
                        color='rgba(54,50,153, 0.5)'),
                    line = dict(
                        width = 2,
                        dash = 'dot'),
                    name='show answer average')

    data = [trace0,trace1,trace2,trace3,trace4,trace5]

    layout = dict(
        title='Activity for User {}'.format(uid),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                dict(count=3,
                     label='3d',
                     step='day',
                     stepmode='backward'),
                dict(count=7,
                     label='1w',
                     step='day',
                     stepmode='backward'),
                dict(count=21,
                    label='3w',
                    step='day',
                    stepmode='backward'),
                dict(count=42,
                    label='6w',
                    step='day',
                    stepmode='backward'),
                dict(step='all')
                ])
            ),
            rangeslider=dict(),
        type='date'
        )
    )
    
    return dict(data = data, layout = layout)




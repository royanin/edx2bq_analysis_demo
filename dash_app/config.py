import pandas as pd
import numpy as np
#from app_db import db, models
from itertools import izip
from datetime import datetime, timedelta

df = pd.read_csv('sample_data/data_person_course_subset.csv')
pcd = pd.read_csv('sample_data/data_person_course_day_subset.csv')
sasby = pd.read_csv('sample_data/data_show_ans_stat_by_user_subset.csv')

df.fillna(0.0, axis=1, inplace=True)
sasby.fillna(0.0, axis=1, inplace=True)

df_col_list =  df.columns.values.tolist()
pcd_col_list =  pcd.columns.values.tolist()
sasby_col_list =  sasby.columns.values.tolist()

#print 'df_col_list:',df_col_list
#print 'pcd_col_list:',pcd_col_list
#print 'sasby_col_list:',sasby_col_list

df_col_list2 = ['nevents', 'ndays_act', 'nplay_video', 'nchapters', 'nforum_posts', 'nforum_votes', 'nforum_endorsed', 'nforum_threads', 'nforum_comments', 'nforum_pinned', 'nprogcheck', 'nproblem_check', 'nforum_events', 'nshow_answer', 'nvideo', 'nvideos_unique_viewed', 'nvideos_total_watched', 'nseq_goto', 'nseek_video', 'npause_video', 'avg_dt', 'sdv_dt', 'max_dt', 'n_dt', 'sum_dt']

df_col_list2_dict = { k:'pct_rank_'+k for k in df_col_list2 }

for item in df_col_list2_dict.keys():
    df[df_col_list2_dict[item]] = df[item].rank(method='average',pct=True).mul(100).round(1)

    
df_col_list =  df.columns.values.tolist()    
#print 'df_col_list:',df_col_list
#print df_col_list2_dict

avg_user = sasby.mean()

avg_attempted = int(avg_user.n_attempted)

max_attempt = sasby.n_attempted.max()

avg_incorrect = int(avg_user.n_attempted) - int(avg_user.n_partial)
avg_partially_correct = int(avg_user.n_partial) - int(avg_user.n_perfect)
avg_correct = int(avg_user.n_perfect)

avg_sa_incorrect = float(avg_user.n_show_answer_attempted) - float(avg_user.n_show_answer_partial)
avg_sa_partially_correct = float(avg_user.n_show_answer_partial) - float(avg_user.n_show_answer_perfect)
avg_sa_correct = float(avg_user.n_show_answer_perfect)

avg_pct_sa_partially_correct = int((avg_sa_partially_correct / avg_partially_correct) * 100)
avg_pct_sa_correct = int((avg_sa_correct / avg_correct) * 100)
avg_pct_sa_incorrect = int((avg_sa_incorrect / avg_incorrect) * 100)


np_username = np.array(df['username'])
np_user_id = np.array(df['user_id'])

user_dict = { k:v for k,v in izip(df['user_id'].tolist(),df['username'].tolist()) }

total = pcd.groupby('date').mean()

date_init = datetime(2012,9,1)
date_last =  datetime(2026,12,29)

all_users = total.groupby('date').sum().reset_index()
all_users.loc[:,('date')] = pd.to_datetime(all_users['date'])

total_days = all_users[(all_users.date >= date_init) & (all_users.date < date_last)]

#STARTING_USER = 534617
STARTING_USER = df['user_id'].iloc[70] #assuming there are about 100 students
#USER_DESCRIPTION = df.loc[df['user_id'] == STARTING_USER].iloc[0]
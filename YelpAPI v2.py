#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:43:56 2018

@author: lalitayang
"""

import os
os.chdir("/Users/lalitayang/Documents/K2/Unit 3/Project/")
print(os.getcwd())

all_friends = load_obj('all_friends')

self_bookmarks = load_obj('self_bookmarks')
my_bm_df = load_obj('my_bm_df')

friend_bookmarks = load_obj('friend_bookmarks')
friend_bm_df = load_obj('friend_bm_df')

my_reviews = load_obj('my_reviews' )
my_review_df = load_obj('my_review_df' )

friend_reviews = load_obj('friends_reviews' )
friend_rev_df = load_obj('friend_rev_df' )

master_biz_ids = load_obj('master_biz_ids')

details = ['alias', 'is_closed', 'price', 'rating', 'review_count', 'id']

###############################################################################
##################### concat all dfs
###############################################################################

master_biz = pd.concat([my_bm_df, my_review_df, friend_bm_df, friend_rev_df])
master_biz_ids = list(set(master_biz['business_id']))
# 16,742 total unique businesses

master_biz_ids.index('robin-san-francisco')

save_obj(master_biz_ids, 'master_biz_ids')
###############################################################################
##################### call business details endpoint for ALL BUSINESSES
##################### Yelp API only allows for 5000 API calls a day
###############################################################################
master_biz_ids = load_obj('master_biz_ids')

master_bizdet_json_4999 = []

for business in master_biz_ids[:5000]:
    df = get_biz_details(CY_api, business)
    master_bizdet_json_4999.append(df)

save_obj(master_bizdet_json_4999, 'master_bizdet_json_4999')
    
master_bizdet_json_9999 = []

for business in master_biz_ids[5000:10000]: 
    df = get_biz_details(JW_api, business)
    master_bizdet_json_9999.append(df)

save_obj(master_bizdet_json_9999, 'master_bizdet_json_9999')

master_bizdet_json_14999 = []

for business in master_biz_ids[10000:15000]:
    df = get_biz_details(api_key, business)
    master_bizdet_json_14999.append(df) 

save_obj(master_bizdet_json_14999, 'master_bizdet_json_14999')

master_bizdet_json_16742 = []

for business in master_biz_ids[15000:]: # still need to run
    df = get_biz_details(PS_api, business)
    master_bizdet_json_16742.append(df) 
    
save_obj(master_bizdet_json_16742, 'master_bizdet_json_16742')
        
###############################################################################
##################### concat all jsons and convert to 1 master dataframe; 
##################### drop duplicates to ensure no duplciates
###############################################################################
    
master_bizdet_json_4999 = load_obj('master_bizdet_json_4999')    
master_bizdet_json_9999 = load_obj('master_bizdet_json_9999')
master_bizdet_json_14999 = load_obj('master_bizdet_json_14999')
master_bizdet_json_16742 = load_obj('master_bizdet_json_16742')

master_bizdet_listdf = []

for business in master_bizdet_json_4999:
    master_bizdet_listdf.append(json_to_df(business, details))

for business in master_bizdet_json_9999:
    master_bizdet_listdf.append(json_to_df(business, details))
  
for business in master_bizdet_json_14999:
    master_bizdet_listdf.append(json_to_df(business, details))
    
for business in master_bizdet_json_16742:
    master_bizdet_listdf.append(json_to_df(business, details))

    
master_bizdet_df = pd.concat(master_bizdet_listdf)
master_bizdet_df.drop_duplicates(subset='alias', keep='first', inplace=True) 

save_obj(master_bizdet_df, 'master_bizdet_df')
master_bizdet_df = load_obj('master_bizdet_df')

master_bizdet_df[master_bizdet_df['alias'].isnull()]

master_bizdet_df = master_bizdet_df.reset_index()
master_biz

###############################################################################
##################### left join with review and bookmark dataframes to get 
##################### business details for each friend/myself
###############################################################################

# need to run the below

for df in [my_bm_df, my_review_df, friend_rev_df, friend_bm_df]:
    df.rename(columns={'id':'user_id'}, inplace=True)
    
for df in [my_review_df, friend_rev_df]:
    df.rename(columns={'rating':'user_rating'}, inplace=True)

my_bm_df2 = pd.merge(my_bm_df, master_bizdet_df, how='left', left_on = 'business_id', right_on='alias')

my_review_df2 = pd.merge(my_review_df, master_bizdet_df, how='left', left_on = 'business_id', right_on='alias')

friend_rev_df2 = pd.merge(friend_rev_df, master_bizdet_df, how='left', left_on = 'business_id', right_on='alias')

friend_bm_df2 = pd.merge(friend_bm_df, master_bizdet_df, how='left', left_on = 'business_id', right_on='alias')

b1 = my_bm_df2[my_bm_df2['alias'].isnull()]
b2 = my_review_df2[my_review_df2['alias'].isnull()]
b3 = friend_rev_df2[friend_rev_df2['alias'].isnull()]
b4 = friend_bm_df2[friend_bm_df2['alias'].isnull()]

blanks = pd.concat([b1, b2, b3, b4])

save_obj(my_bm_df2, 'my_bm_df2')
save_obj(my_review_df2, 'my_review_df2')
save_obj(friend_rev_df2, 'friend_rev_df2')
save_obj(friend_bm_df2, 'friend_bm_df2')





s
































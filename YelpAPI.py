#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:43:56 2018

@author: lalitayang
"""

import os
os.chdir('/Users/lalitayang/Documents/K2/Unit 3/Project/')
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

details = ['alias', 'is_closed', 'price', 'rating', 'review_count']

###############################################################################
##################### call business details endpoint for my BOOKMARKS
###############################################################################

my_bm_details = []

for business in my_bm_df['business_id']:
    df = get_biz_details(api_key, business)
    my_bm_details.append(df)

my_bm_details_df = []

for business in my_bm_details:
    my_bm_details_df.append(json_to_df(business, details))
    
# create dataframe of details i want
my_bm_det_df = pd.concat(my_bm_details_df)

###############################################################################
##################### concat all dfs
###############################################################################

master_biz = pd.concat([my_bm_df, my_review_df, friend_bm_df, friend_rev_df])
master_biz_ids = list(set(master_biz['business_id']))
# 16,742 total unique businesses

###############################################################################
##################### call business details endpoint for ALL BUSINESSES
##################### Yelp API only allows for 5000 API calls a day
###############################################################################

master_bizdet_json_4999 = []

for business in master_biz_ids[:5000]:
    df = get_biz_details(api_key, business)
    master_bizdet_json_4999.append(df)

save_obj(master_bizdet_json_4999, 'master_bizdet_json_4999')
    
master_bizdet_json_9999 = []

for business in master_biz_ids[5000:10000]:
    df = get_biz_details(api_key, business)
    master_bizdet_json_9999.append(df)

save_obj(master_bizdet_json_9999, 'master_bizdet_json_9999')

master_bizdet_json_14999 = []

for business in master_biz_ids[10000:15000]: # still need to run
    df = get_biz_details(api_key, business)
    master_bizdet_json_14999.append(df) 
    
master_bizdet_json_16742 = []

for business in master_biz_ids[15000:]: # still need to run
    df = get_biz_details(api_key, business)
    master_bizdet_json_16742.append(df) 

###############################################################################
##################### concat all jsons and convert to 1 master dataframe; 
##################### drop duplicates to ensure no duplciates
###############################################################################
    
master_bizdet_listdf = []

for business in master_bizdet_json_4999:
    master_bizdet_listdf.append(json_to_df(business, details))

for business in master_bizdet_json_9999:
    master_bizdet_listdf.append(json_to_df(business, details))
    
master_bizdet_df = pd.concat(master_bizdet_listdf)
master_bizdet_df.drop_duplicates() 

save_obj(master_bizdet_df, 'master_bizdet_df')
    
###############################################################################
##################### call business details endpoint for my REVIEWS
###############################################################################

my_rev_det_df = api_to_df(api_key, details, my_review_df)

###############################################################################
##################### call business details endpoint for FRIENDS REVIEWS
###############################################################################

# don't need duplicates
friends_bm_set = list(set(all_rev_df.business_details))
review_diff = list((set(all_rev_df['business_details']).difference(set(my_rev_det_df.alias))))

###############################################################################
##################### SAVE YELP API BUSINESS DETAILS
###############################################################################

my_bm_det_df = load_obj('my_bookmarks_biz_details')

save_obj(my_bm_det_df, 'my_bookmarks_biz_details')
save_obj(my_rev_det_df, 'my_reviews_biz_details')
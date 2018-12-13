#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 13:58:47 2018

@author: lalitayang
"""

from sklearn.metrics import pairwise_distances

r_sim = pairwise_distances(features.fillna(0), metric='cosine')
r_sim = pd.DataFrame(r_sim[:,-1], index=features.index, columns=['similarity']).sort_values('similarity')

save_obj(r_sim, 'r_sim')

# get top 3 similar users
top = list(r_sim.index[:4])

# dataframe for only 3 users and their bookmarked & reviewed businesses to get recs
ids = ['user_id', 'business_id']
names = pd.concat([df.loc[:, ids] for df in [friend_bm_df2, friend_rev_df2, my_bm_df2, my_review_df2]] )
names = names.loc[names['user_id'].isin(top)]
names['count'] = 1

recs = pd.pivot_table(names, index='business_id', columns='user_id', values='count', aggfunc=np.sum, fill_value = 0)

temp = recs[recs[self_id]==0].copy() # businesses I have not bookmarked/reviewed
temp2 = temp.loc[:,temp.columns != self_id].copy() # remove myself
str_recs = temp2[temp2.sum(axis=1)>2] # businesses that all 3 have been to

# merge recs with business details api
rec_details = pd.DataFrame(index= str_recs.index)
rec_details = pd.merge(rec_details, right=master_bizdet_df, how='left', left_index=True, right_on='alias')

# don't want recommendations for businsses that are closed and filter for greater than 4 stars
rec_details = rec_details[rec_details['is_closed']==False][rec_details['rating']>4]
rec_details['price_val'] = rec_details['price'].apply(lambda x: count_dollar_sign(x))
save_obj(rec_details, 'rec_details')

cat_bar_plot(rec_details, 'Recommendations Bar Chart', 10)
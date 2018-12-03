#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 13:58:47 2018

@author: lalitayang
"""

def calc_sim(df, self_id, sim_type):
    """ function to calculate similarity between users using pearson r
        returns a sorted dataframe of similarities and users"""
    sim_score = {}
    df = df.fillna(0)
    for i in df.index:
        ss = pearsonr(df.loc[self_id,:], df.loc[i,:])
        sim_score.update({i: ss[0]})
    
    sim = pd.Series(sim_score).to_frame(sim_type+'_similarity')
    sim_sorted = sim.sort_values(sim_type+'_similarity', ascending=False)
    return sim_sorted

    
rev_sim = calc_sim(reviews, self_id, 'rev')
bm_sim = calc_sim(bookmarks, self_id, 'bm')

# total and average the similarities
both_sim = bm_sim.join(rev_sim)
both_sim['total'] = both_sim.sum(axis=1)
both_sim['avg'] = both_sim['total']/2
both_sim = both_sim.sort_values('avg', ascending=False)

save_obj(both_sim, 'both_sim')

# get top 3 similar users
top = list(both_sim.index[:4])

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

# don't want recommendations for businsses that are closed
rec_details = rec_details[rec_details['is_closed']==False]
rec_details['price_val'] = rec_details['price'].apply(lambda x: count_dollar_sign(x))
save_obj(rec_details, 'rec_details')

cat_bar_plot(rec_details, 'Recommendations Bar Chart', 10)
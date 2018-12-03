#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:16:39 2018

@author: lalitayang
"""

import matplotlib.pyplot as plt

####################################################################
################ PLOT CATEGORIES
####################################################################   

def cat_bar_plot(df, name, topN):
    """ function to plot bar chart of top N categories"""
    
    cat_dict = {}    
    cats = [df['cat_0'], df['cat_1'], df['cat_2'], df['cat_3'], df['cat_4']]
    
    for cat in cats:
        for c in cat:
            if c not in cat_dict.keys():
                cat_dict[c] = 1
            else: 
                cat_dict[c] += 1
                        
    cats_df = pd.Series(cat_dict).to_frame()
    cats_df.reset_index(inplace=True)
    cats_df.columns = ['category', 'count']
    cats_df.dropna(axis=0, how='any', inplace=True)
    cats_df.sort_values(by='count', ascending=False, inplace=True)
    
    plt.figure(figsize=(10,10))
    cats_df[:topN].plot.bar(x='category', y='count')
    plt.title(name)
    plt.xlabel('category')
    plt.ylabel('count')
    plt.savefig('./Yelp Pics/'+name+'.png', bbox_inches='tight' )

# plot master, my bookmraks, my reviews    
cat_bar_plot(master_bizdet_df, 'All Categories Bar Chart', 10)
cat_bar_plot(my_bm_df2, 'My Bookmarks_Category Bar Chart', 10)
cat_bar_plot(my_review_df2, 'My Reviews_Category Bar Chart', 10)


####################################################################
################ GET STATISTICS OF MASTER DATAFRAME
####################################################################   

master_bizdet_df['price_val'] = master_bizdet_df['price'].apply(lambda x: count_dollar_sign(x))

save_obj(master_bizdet_df, 'master_bizdet_df2')

master_bizdet_df.describe()
# at least 75% of the businesses have 4 stars or higher 
# most of the businesses are 2 dollar signs or less
# review_count buckets:
    # lesser known = < 50
    # average popularlity = 50 - 500
    # popular = 500+ 
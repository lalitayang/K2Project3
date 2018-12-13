#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:16:39 2018

@author: lalitayang
"""

import matplotlib.pyplot as plt

####################################################################
################ PLOT CATEGORIES - bar chart
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
################ PLOT CATEGORIES - histogram
####################################################################   

def top_cats(df, topN):
    """ function to find top N categories"""
    
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
    
    return cats_df[:topN]

top_overall_cats = top_cats(master_bizdet_df, 10)

def cat10_hist_compare(top_overall_cats, friend_features, my_features, subplots, name):
    """ function to plot 10 yelp categories and highlight where an individual stands"""
    data = friend_features.loc[:, top_overall_cats['category']]
    my_data = my_features.loc[:, top_overall_cats['category']]

    f,a = plt.subplots(5, 2, figsize=(10,25))
    a = a.ravel()
    for idx, ax in enumerate(a):
        data.iloc[:,idx].hist(ax=ax, bins=20)
        ax.set_title(data.columns[idx])
        ax.set_xlabel('Proportion of Bookmarks & Reviews')
        ax.set_ylabel('Count of Users')
        ax.axvline(x=my_data.iloc[:,idx][0], color='r', linestyle='--')
    plt.tight_layout()
    
    plt.savefig('./Yelp Pics/'+name+'.png', bbox_inches='tight' )
    
cat10_hist_compare(top_overall_cats, friend_features, my_features, subplots = 'top10_histogram')

####################################################################
################ PLOT CATEGORIES - box plot
####################################################################   
def plot_topcat_box(friend_features, my_features):
    data = friend_features.loc[:, top_overall_cats['category']]
    my_data = my_features.loc[:, top_overall_cats['category']]
    
    plt.figure(figsize=(15,15))
    data.boxplot()
    for i in range(10):
        y = my_data.iloc[:,i][0]
        x = i
        plt.plot(x, y, 'ro')
        
    plt.savefig('./Yelp Pics/cat10_boxplot.png', bbox_inches='tight')
    
plot_topcat_box(friend_features, my_features)

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
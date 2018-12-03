#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:03:20 2018

@author: lalitayang
"""

bookmark_url = 'https://www.yelp.com/user_details_bookmarks?userid='
review_url = 'https://www.yelp.com/user_details_reviews_self?userid='
friends_url = 'https://www.yelp.com/user_details_friends?userid='

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pickle
import json

from sklearn.metrics import jaccard_similarity_score
from scipy.stats import pearsonr

def save_obj(obj, name ):
    """ save object """
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    """ load object """
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
  
####################################################################
################ SCRAPING FUNCTIONS
####################################################################     

def first_page_friends(user_id):
    """function to get the User IDs of the first page of friends"""

    f_page = requests.get(friends_url + user_id)
    f_soup = BeautifulSoup(f_page.content, 'html.parser')
    f_source = f_soup.find_all('a', class_='user-display-name js-analytics-click')
    
    friend_list = []
    for friend in range(0, len(f_source)):
        friend_id = f_source[friend]['href'].split('=')[1]
        friend_list.append(friend_id)
    
    return friend_list

def get_all_friends(user_id):
    """function to get the User IDs of all friends"""
    
    # get the max page number of bookmarks
    friendpage = requests.get(friends_url+user_id)
    fr_soup = BeautifulSoup(friendpage.content, 'html.parser')
    pages = fr_soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')
    max_page = pages[0].get_text().split('of ')[1].split('\n')[0]
    friend_list = []   
    #get friends
    for page_num in range(0,48*int(max_page), 48):
        f_page = requests.get(friends_url + user_id+ '&start=' + str(page_num))
        f_soup = BeautifulSoup(f_page.content, 'html.parser')
        f_source = f_soup.find_all('a', class_='user-display-name js-analytics-click')
    
        for friend in range(0, len(f_source)):
            friend_id = f_source[friend]['href'].split('=')[1]
            friend_list.append(friend_id)

    return friend_list

def get_bookmarks(user_id):
    """get all bookmarks for user_id"""

    user_bookmarks = []
     
    try: # not all accounts have the bookmarks as public data       
   
        # get the max page number of bookmarks
        bookmarks = requests.get(bookmark_url+user_id)
        bm_soup = BeautifulSoup(bookmarks.content, 'html.parser')
        pages = bm_soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')
        max_page = pages[0].get_text().split('of ')[1].split('\n')[0]

        # loop through all the pages to get bookmarks
        for page_num in range(0, 50*int(max_page), 50):
            bookmarks = requests.get(bookmark_url + user_id + '&start=' + str(page_num))
            bm_soup = BeautifulSoup(bookmarks.content, 'html.parser')
            bm_name = bm_soup.find_all('a', class_='biz-name js-analytics-click')

            for mark in range(0, len(bm_name)):
                user_bookmarks.append(bm_name[mark]['href'])
        
        return user_bookmarks
    
    except: 
        return [np.nan]
       
def get_bookmarks(user_id):
    """get all bookmarks for user_id"""

    user_bookmarks = []
     
    try: # not all accounts have the bookmarks as public data       
   
        # get the max page number of bookmarks
        bookmarks = requests.get(bookmark_url+user_id)
        bm_soup = BeautifulSoup(bookmarks.content, 'html.parser')
        pages = bm_soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')
        max_page = pages[0].get_text().split('of ')[1].split('\n')[0]

        # loop through all the pages to get bookmarks
        for page_num in range(0, 50*int(max_page), 50):
            bookmarks = requests.get(bookmark_url + user_id + '&start=' + str(page_num))
            bm_soup = BeautifulSoup(bookmarks.content, 'html.parser')
            bm_name = bm_soup.find_all('a', class_='biz-name js-analytics-click')

            for mark in range(0, len(bm_name)):
                user_bookmarks.append(bm_name[mark]['href'])
        
        return user_bookmarks
    
    except: 
        return [np.nan]
       


def biz_id_bookmarks(user_id):
    """get all bookmarks for user_id"""

    bizid_bookmarks = []
     
    try: # not all accounts have the bookmarks as public data       
   
        # get the max page number of bookmarks
        bookmarks = requests.get(bookmark_url+user_id)
        bm_soup = BeautifulSoup(bookmarks.content, 'html.parser')
        pages = bm_soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')
        max_page = pages[0].get_text().split('of ')[1].split('\n')[0]

        # loop through all the pages to get bookmarks
        for page_num in range(0, 50*int(max_page), 50):
            bookmarks = requests.get(bookmark_url + user_id + '&start=' + str(page_num))
            bm_soup = BeautifulSoup(bookmarks.content, 'html.parser')
            biz_id = bm_soup.find_all('a', class_='biz-name js-analytics-click')

            for mark in range(0, len(biz_id)):
                bizid_bookmarks.append(biz_id[mark]['data-hovercard-id'])
           
    except: 
        bizid_bookmarks.append(np.nan)

    return bizid_bookmarks

    
def biz_id_reviews(user_id):
        
    r_biz_id = []
    
    try: # not all accounts have the reviews    
        
        # get the max page number of reviews
        reviews = requests.get(review_url+user_id)
        re_soup = BeautifulSoup(reviews.content, 'html.parser')
        pages = re_soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')
        max_page = pages[0].get_text().split('of ')[1].split('\n')[0]
        
        # loop through all the pages to get reviews   
        for page_num in range(0, 10*int(max_page), 10):
            rev = requests.get(review_url + user_id + '&rec_pagestart=' + str(page_num))
            rev_soup = BeautifulSoup(rev.content, 'html.parser')
            #rating = rev_soup.find_all('div', class_=re.compile('i-stars i-stars--regular-*'))
            biz_id = rev_soup.find_all('a', class_='biz-name js-analytics-click')

            for mark in range(0, len(biz_id)):
                r_biz_id.append(biz_id[mark]['data-hovercard-id'])

    except:
        r_biz_id.append(np.nan)
    
    return r_biz_id   

def get_reviews(user_id):
    """get all reviews for user_id"""
    user_reviews = {}    
    
    try:
        # get the max page number of bookmarks
        reviews = requests.get(review_url+user_id)
        re_soup = BeautifulSoup(reviews.content, 'html.parser')
        pages = re_soup.find_all('div', class_='page-of-pages arrange_unit arrange_unit--fill')
        max_page = pages[0].get_text().split('of ')[1].split('\n')[0]


        # loop through all the pages to get bookmarks
        for page_num in range(0, 10*int(max_page), 10):
            rev = requests.get(review_url + user_id + '&rec_pagestart=' + str(page_num))
            rev_soup = BeautifulSoup(rev.content, 'html.parser')
            rating = rev_soup.find_all('div', class_=re.compile('i-stars i-stars--regular-*'))
            biz_name = rev_soup.find_all('a', class_='biz-name js-analytics-click')

            for mark in range(0, len(biz_name)):
                user_reviews[biz_name[mark]['href']] = int(rating[mark]['title'][0])
   
    except:
        pass # pass for users with no reviews
    
    return user_reviews
   
def split_biz_url(url):
    """ helper function to get the unique business name 
        by splitting /biz/ out from scraped data"""
    try:
        return url.split('/biz/')[1]       
    except:
        pass

def create_df_bookmarks(key, bookmarks):
    """ helper function to create dataframe of bookmarks from friends scraped data for list of dataframes"""
    df = pd.DataFrame(bookmarks[key], columns=['url'])
    df['id'] = key
    df['business_id'] = df['url'].apply(lambda x: split_biz_url(x))
    return df

def create_df_reviews(key, reviews):
    """ create dataframe of reviews from scraped data"""
    df = pd.DataFrame(list(reviews[key].items()), columns=['url', 'rating'])
    df['id'] = key
    df['business_id'] = df['url'].apply(lambda x: split_biz_url(x))
    return df
    
####################################################################
################ API CALL FUNCTIONS
####################################################################      

    
def get_biz_details(api_key, business):
    """ call business details endpoint of yelp api and returns a json object"""
    try:
        url = 'https://api.yelp.com/v3/businesses/{}'.format(business)
        headers = {'Authorization' : 'Bearer %s' % api_key}
        resp = requests.get(url=url, headers=headers)
        return resp.json()
    except:
        pass

def json_to_df(business, details):
    """ create dataframe from json object after calling api endpoint for specific details """
    df_dict = {}
    for det in details:
        try:        
            df_dict[det] = [business[det]]
        except:
            pass
    try:
        cats = {'cat_{}'.format(i):[business['categories'][i]['alias']] for i in range(len(business['categories']))}
        df_dict.update(cats)
    except:
        pass
    return pd.DataFrame(df_dict)

def api_to_df(api_key, details, business_ids):
    """ uses the json_to_df and get_biz_details functions to
            first call business details endpoint from yelp api
            then returns a dataframe based on details desired
    """
    api_call = []

    for business in business_ids:
        biz_details = get_biz_details(api_key, business)
        api_call.append(biz_details)    
    
    df_temp = []

    for business in api_call:
        df_temp.append(json_to_df(business, details))
        
    biz_details_df = pd.concat(df_temp)
    
    return biz_details_df

####################################################################
################ FEATURE ENGINEERING FUNCTIONS
####################################################################  
    
def count_dollar_sign(price):
    """ helper func to convert $ price to numeric """
    try:
        x = len(price)
        return x
    except:
        pass
    
def count_categories(df, usr_id):
    """ function to count the number of businesses for each category """
    cat_dict = {}    
    cats = [df['cat_0'], df['cat_1'], df['cat_2'], df['cat_3'], df['cat_4']]

    for cat in cats:
        for c in cat:
            if c not in cat_dict.keys():
                cat_dict[c] = 1
            else: 
                cat_dict[c] += 1
                        
    s = pd.Series(cat_dict).to_frame().T
    s = s.loc[:, s.columns.notnull()]
    s.index = [usr_id]          
    s['num'] = len(df[df['user_id'] == usr_id].index)      
    return s

def get_features(df, usr_id):
    """ function to create a dataframe that has:
        - average price for businesses interested in
        - average rating of businesses interested in
        - uses count_categories """
    temp = df[df['user_id'] == usr_id]
    temp1 = temp.copy()
    try: 
        temp1['price_val'] = temp1['price'].apply(lambda x: count_dollar_sign(x))
        left = pd.pivot_table(temp1, values=['price_val', 'rating'], aggfunc='mean', index='user_id')
    except:
        print('left fail', usr_id)
    try:
        right = count_categories(temp1, usr_id)
        right = right.apply(lambda x: x/x.loc['num'], axis=1) # normalize and get % of reviews are x category
    except:
        print('right fail', usr_id)
    try:
        features = left.merge(right, how='inner', left_index=True, right_index=True)
    except:
        print('merge fail', usr_id)
    try:    
        return features
    except:
        pass

####################################################################
################ EDA FUNCTIONS
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

####################################################################
################ CALCULATE SIMILARITY FUNCTIONS
####################################################################   
    
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
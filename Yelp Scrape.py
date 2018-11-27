#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:11:54 2018

@author: lalitayang
"""
import os
os.chdir('/Users/lalitayang/Documents/K2/Unit 3/Project/')

###############################################################################
##################### GET LIST OF ALL FRIENDS 
###############################################################################
all_friends = get_all_friends(self_id) # LIST

###############################################################################
##################### BOOKMARKS to dataframe
###############################################################################

# scrape my own bookmarks - LIST
self_bookmarks = get_bookmarks(self_id)

# create dataframe for my own bookmarks
my_bm_df = pd.DataFrame({'url': self_bookmarks,
                         'id' : self_id,
                         'business_id' : [bm.split('/biz/')[1] for bm in self_bookmarks]})

# create dictionary of users and their scraped bookmarks
friend_bookmarks = {i:[] for i in all_friends}

for i in all_friends:
    friend_bookmarks[i] = get_bookmarks(i)

# create dataframe for friends bookmarks  

friend_bm_df = [create_df_bookmarks(key, friend_bookmarks) for key in friend_bookmarks.keys()]
friend_bm_df = pd.concat(friend_bm_df)


###############################################################################
##################### REVIEWS
###############################################################################

# scrape my own reviews - DICT
my_reviews = get_reviews(self_id)

# create dataframe for my reviews
my_review_df = pd.DataFrame(list(my_reviews.items()), columns=['url', 'rating'])
my_review_df['id'] = self_id
my_review_df['business_id'] = my_review_df['url'].apply(lambda x: split_biz_url(x))

# create dictionary of all users and their reviews - dict of dicts
friend_reviews = {i:[] for i in all_friends}

for i in all_friends:
    friend_reviews[i] = get_reviews(i)
   
# create dataframe for friend reviews
friend_rev_df = [create_df_reviews(key, friend_reviews) for key in friend_reviews.keys()]
friend_rev_df = pd.concat(friend_rev_df)


###############################################################################
##################### SAVE ALL SCRAPED DATA
###############################################################################

save_obj(all_friends, 'all_friends')

save_obj(self_bookmarks, 'self_bookmarks')
save_obj(my_bm_df, 'my_bm_df')

save_obj(friend_bookmarks, 'friend_bookmarks')
save_obj(friend_bm_df, 'friend_bm_df')

save_obj(my_reviews, 'my_reviews' )
save_obj(my_review_df, 'my_review_df' )

save_obj(friend_reviews, 'friends_reviews' )
save_obj(friend_rev_df, 'friend_rev_df' )


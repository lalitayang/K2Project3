# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:24:23 2018

@author: lalyang
"""

master_bizdet_df = load_obj('master_bizdet_df')
my_bm_df2 = loab_obj('my_bm_df2')
my_review_df2 = loab_obj('my_review_df2')
friend_rev_df2 = loab_obj('friend_rev_df2')
friend_bm_df2 = loab_obj('friend_bm_df2')   
        
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


### create dataframes containing features
        
friend_bm_features = []
friend_rev_features = []

for friend in all_friends:
    features = get_features(friend_bm_df2, friend)
    friend_bm_features.append(features)

for friend in all_friends:   
    fet = get_features(friend_rev_df2, friend)
    friend_rev_features.append(fet)
    

friend_bm_features = pd.concat(friend_bm_features)
friend_rev_features = pd.concat(friend_rev_features)

my_bm_features = get_features(my_bm_df2, self_id)
my_rev_features = get_features(my_review_df2, self_id)

### concatenate all bookmarks and all reviews
reviews = friend_rev_features.append(my_rev_features)
bookmarks = friend_bm_features.append(my_bm_features)

save_obj(my_rev_features, 'my_rev_features')
save_obj(my_bm_features, 'my_bm_features')
save_obj(friend_bm_features, 'friend_bm_features')
save_obj(friend_rev_features, 'friend_rev_features')
















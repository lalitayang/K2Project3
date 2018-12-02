# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:24:23 2018

@author: lalyang
"""

master_bizdet_df.describe()
# at least 75% of the businesses have 4 stars or higher 
# most of the businesses are 2 dollar signs or less
# review_count buckets:
    # lesser known = < 50
    # average popularlity = 50 - 500
    # popular = 500+ 
    
master_bizdet_df['price_val'] = master_bizdet_df['price'].apply(lambda x: count_dollar_sign(x))

def count_dollar_sign(price):
    try:
        x = len(price)
        return x
    except:
        pass
    


def count_categories(df):
    cat_dict = {}    
    cats = [df['cat_0'], df['cat_1'], df['cat_2'], df['cat_3'], df['cat_4']]

    for cat in cats:
        for c in cat:
            if c not in cat_dict.keys():
                cat_dict[c] = 1
            else: 
                cat_dict[c] += 1
                
    return pd.DataFrame(cat_dict, index=df['user_id']).drop_duplicates()

def get_features(df, usr_id):
    temp = df[df['user_id'] == usr_id]
    temp1 = temp.copy()
    try: 
        temp1['price_val'] = temp1['price'].apply(lambda x: count_dollar_sign(x))
        left = pd.pivot_table(temp1, values=['price_val', 'rating'], aggfunc='mean', index='user_id')
    except:
        print('left fail', usr_id)
    try:
        right = count_categories(temp1)
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

?pd.pivot_table

master_cat_dict = count_categories(master_bizdet_df)

mybm_catdict = count_categories(my_bm_df2)

my_bm_df2['price_val'] = my_bm_df2['price'].apply(lambda x: count_dollar_sign(x))
test = pd.pivot_table(my_bm_df2, values=['price_val', 'rating'], aggfunc='mean', index = 'user_id')
test2 = test.merge(mybm_catdict, how='inner', left_index=True, right_index=True)

?pd.merge

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




friend_rev_df2.loc[friend_rev_df2['user_id'=='Htjd8quvxKquXyKG27bDWw']]































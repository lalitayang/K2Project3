# K2Project3

# Yelp Recommendation Engine: 

## Background:
Yelp is a local-search serviced powered by crowd-sourced reviews of local businesses. I am a frequent visitor of Yelp and rely heavily on the reviews to make decisions on which restaurants to visit, what to order at the restaurant, and outside of food, I also rely on Yelp reviews for services I seek. In addition to leaving reviews with a rating between 1-5, users with an account with Yelp are able to add friends and to create Bookmarks for businesses they want to visit in the future and can refer to later. Yelp also has their own API has various endpoints that provide different information related to businesses, events, and categories.

## Purpose: 
To build a recommendation system for Yelp using bookmarks and review ratings and the users that are most similar to me.

I spend a lot of time going through Yelp trying to find a place to eat, especially if I am not craving anything in particular. With a recommendation engine, I can narrow down the list of places that I may enjoy.

### Scripts
1. YelpFunctions.py - contains all functions used throughout project
2. Yelp Scrape.py - script to scrape www.yelp.com for user IDs and business names
3. YelpAPI v2.py - script to call the Business Details endpoint of Yelp Fusion API using business names
4. YelpFeatureEngineering.py - script to clean data and create features to be used in calculating similarity
5. YelpEDA.py - script to explore data and business categories
6. YelpSim.py - script to calculate similarity between users and extract recommendations

### Jupyter Notebook
7. Yelp_Recommendation_Final.ipynb - jupyter notebook to put it all together and for analysis

### Folders
8. obj folder - saved objects from analysis
9. Yelp Pics folder - saved graphs

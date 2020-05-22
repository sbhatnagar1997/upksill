"""
Author: Shubham Bhatnagar
Date Created: 01/05/2020

Purpose: Twitter interaction using webscraping with TWINT
- https://github.com/twintproject/twint 
"""

#%%
# =============================================================================
# Imports
# =============================================================================
import pycountry
import time
import json

import twint
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Defining Functions
# =============================================================================

# Function that creates a list of search terms    
def search_creator(country_state_list,term):
    
    cs = country_state_list.copy()
    
    # for every state in every country, prepend the 'term'
    for k,v in cs.items():
        if k.lower() != 'singapore':
            v = [term+ ' ' + x for x in v]
            cs[k] = v
        else:
            v = [term + ' singapore ' + x for x in v]
            cs[k] = v

    return cs        


#%%
# =============================================================================
# Creating country list
# =============================================================================

# List of countries we want to search through

# This is the original list
# country_list=['germany','china','united kingdom','spain','italy','singapore','hong kong','us']

# country_list=['italy','singapore','hong kong','us']

# The following country_list is an input based version
country_list = [str(input('Enter name of country: '))]

# Creating a list of all countries/states and their codes
countries = pycountry.countries
states  =pycountry.subdivisions

# Mapping country code to country (identifying any errors)
country_code = {}
error = []

for c in country_list:
    try:
        country_code[c] = countries.lookup(c).alpha_2
    except:
        error.append(c)

if len(error):
    print('These countries did not work: ',error)
else:
    print('All countries worked, check state list to confirm.')
        
# Mapping state name to country code

# empty dictionary to store country, code list
country_state= {}

# Iterating through every country
for k,v in country_code.items():
    curr_states = list(states.get(country_code=v)) # all states for curr 
    
    temp = []
    temp.append(k)
    
    for c in curr_states:
        temp.append(c.name)    
    
    country_state[k] = temp
    

search = search_creator(country_state,'covid')

#%%
# =============================================================================
# Searching twitter using TWINT
# =============================================================================

GeoLocation = {'singapore':'1.3521, 103.8198,{}','hong kong':'22.3193, 114.1694,{}','germany':'51.1657, 10.4515,{}','italy':'41.8719, 12.5674,{}','china':'35.8617, 104.1954,{}','united kingdom':'55.3781, 3.4360,{}','us':'37.0902, 95.7129,{}','spain':'40.4637, 3.7492,{}'}

# Dictionary for number of tweets per subdivision per country
NumTweets = {'singapore':250,'hong kong':1000,'germany':50,'italy':50,'china':1000,'united kingdom':5,'us':50,'spain':50, 'chile':1}

results = {}
for k,v in search.items():
    temp = []    
    store_d = {}
    print('Searching Tweets related to {}'.format(k))

    for t in v:
        tweets = []       
        c = twint.Config()
        c.Hide_output = True
        c.Search = "{}".format(t)
        try:
            c.Limit = NumTweets[k]
        except:
            c.Limit = 20
        c.Store_object = True  
        c.Lang = 'en'
        #km = '10km'
        #c.Geo = GeoLocation[k].format(km)

        c.Store_object_tweets_list = tweets
        twint.run.Search(c)   
                
        # Saving relevant tweet metadata as json object
        for obj in tweets:
            store_d[obj.conversation_id] = {'datetime':obj.datetime,'likes':obj.likes_count, 'retweets':obj.retweets_count,'tweet':obj.tweet,'analyzed':0,'sentiment':''}

        temp = temp + tweets # adding all tweets from one country into list
    
    # Saving all data as JSON
    key = k.replace(' ','_')
    # Reading the file to see what old data there is
    # If it exists, read the previous data and add new to it
    try:
        with open(r'./json/json_{}.txt'.format(key),'r', encoding='utf-8') as f:
            # loading previous data
            import ipdb; ipdb.set_trace()
            prev = json.load(f)

            # If the same tweet does not exist, then add it to list
            for k,v in store_d.items():
                if k not in prev.keys():
                    prev[k] = v

            f.close()
    # If it doesnt exist, just take the new data
    except:
        prev = store_d

    # re-writing the file to store the new data
    with open(r'./json/json_{}.txt'.format(key),'w', encoding='utf-8') as f:
        # Storing all the data
        json.dump(prev, f, ensure_ascii=True, indent=4)
        f.close()







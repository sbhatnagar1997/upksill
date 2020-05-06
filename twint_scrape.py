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

import twint
import nest_asyncio
nest_asyncio.apply()

#%%
# =============================================================================
# Creating country list
# =============================================================================

# List of countries we want to search through

# This is the original list
#country_list=['germany','china','united kingdom','spain','italy','singapore','hong kong',
#               'us']

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

search = search_creator(country_state,'covid')

#%%
# =============================================================================
# Searching twitter using TWINT
# =============================================================================

GeoLocation = {'singapore':'1.3521, 103.8198,{}','hong kong':'22.3193, 114.1694,{}','germany':'51.1657, 10.4515,{}','italy':'41.8719, 12.5674,{}','china':'35.8617, 104.1954,{}','united kingdom':'55.3781, 3.4360,{}','us':'37.0902, 95.7129,{}','spain':'40.4637, 3.7492,{}'}


results = {}
for k,v in search.items():
    temp = []    
    print('Searching Tweets related to {}'.format(k))

    for t in v:
        tweets = []       
        c = twint.Config()
        c.Hide_output = True
        c.Search = "{}".format(t)
        c.Limit = 10
        c.Store_object = True  
        c.Lang = 'en'
        #km = '10km'
        #c.Geo = GeoLocation[k].format(km)

        c.Store_object_tweets_list = tweets
        twint.run.Search(c)   
                
        temp = temp + tweets # adding all tweets from one country into list
    
    # Saving into text file
    key = k.replace(' ','_')
    with open(r'./Tweets/tweets_{}.txt'.format(key),'wb') as f:
        for t in temp:                 
            f.write(t.tweet.encode('utf-8'))
            f.write('\n'.encode('utf-8'))            
            f.write('-----Line of Text------------'.encode('utf-8'))
            f.write('\n'.encode('utf-8'))
        f.close()






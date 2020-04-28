"""
Author: Shubham Bhatnagar
Date Created: 25/04/2020

Purpose: Twitter API interaction script using python-twitter 
documentation: https://python-twitter.readthedocs.io/en/latest/index.html 

Issues:

1) The geot-tagging of tweets is not functional anymore (twitter deprectted)
the functionality.
- SOLN: New method is going to be trying to search for key terms related to 
country
"""

#%%
# =============================================================================
# Imports
# =============================================================================
import twitter
import pycountry
import os

# Loading in environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

#%%
# =============================================================================
# Creating connection to Twitter API
# =============================================================================

# Authentication codes
ck = os.environ.get('CONSUMER_KEY')
cks = os.environ.get('CONSUMER_KEY_SECRET')
ak = os.environ.get('ACCESS_KEY')
aks = os.environ.get('ACCESS_KEY_SECRET')

# Authorizing access Oauth 1a (although could probably use 2)
api = twitter.Api(consumer_key=ck,
                  consumer_secret=cks,
                  access_token_key=ak,
                  access_token_secret=aks)


#%%
# =============================================================================
# Create search parameters using Pycountry
# =============================================================================
# List of countries we want to search through
country_list=['germany','china','uk','spain','italy','singapore','hong kong',
              'us']

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

print('These countries did not work: ',error)
        
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
    
    for k,v in cs.items():
        v = [term+ ' ' + x for x in v]
        cs[k] = v

    return cs        

search = search_creator(country_state,'covid')




#%%
# =============================================================================
# Searching for tweets
# =============================================================================

results = []
for t in search['germany']:
    results.append(api.GetSearch(term=t,lang='en',count=100,
                                 result_type='mixed'))
    
#%%
# =============================================================================
# Printing results
# =============================================================================

count = 0
for r in results:
    for r2 in r:
        print(r2.text + '\n')
        count += 1
        


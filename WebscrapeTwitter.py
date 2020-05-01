"""
Author: Shubham Bhatnagar
Date Created: 28/04/2020

Purpose: Twitter interaction using webscraping
- Tring to bypass rate limit
"""

#%%
# =============================================================================
# Imports
# =============================================================================
import pycountry
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs


#%%
# =============================================================================
# Selenium
# =============================================================================
# need to use an authenticated webdriver!    

def search_twitter(term):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    # Load twitter webpage
    driver.get(r'https://www.twitter.com/explore')
    
    # Sleep to allow page load
    time.sleep(2)
    
    xpath = r'//input[@data-testid="SearchBox_Search_Input"]' 
    
    driver.find_element_by_xpath(xpath).send_keys('{}'.format(term), Keys.ENTER)
    
    # Sleep to allow page load
    time.sleep(2)
    
    # Scrolling down and finding different tweets#
    
    # Different class attribute values
    
    # New tweet
    nt = 'css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0' 
    
    # Text in tweet
    t1 = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'
    
    # term in tweet
    # t2 = 'css-901oao css-16my406 r-1qd0xha r-vw2c0b r-ad9z0x r-bcqeeo r-qvutc0'
    
    n = 50
    all_r = []
    for i in range(n):
        
        driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

        html = driver.page_source
        soup = bs(html, 'html.parser')
        
        
        #ll all script and style elements

        for script in soup(["script", "style"]):
                script.extract()    # rip it out

            
        # get text
        text = soup.get_text()
        #break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
        new_lines = []
        
        for l in chunks:                        
            if "Twitter Search" in l or "JavaScript" in l or not l:
                pass
            else:
                new_lines.append(l)
                
       
        # Check if text doesnt already exist.
        text = [t for t in new_lines if t not in all_r]
        
        # Need to encode results to avoid repetition    
        all_r = all_r + text
    
        
    # Old way to try and find text
    #result = soup.find_all(name='div',attrs={'class':nt})
    
    #for tweet in result:
        
    #    temp = tweet.find_all(name='span', attrs={'class':t1})
        
    #    t = [te.text for te in temp]
    #    all_r.append(t)
    
    #all_r.append(result)
    
    driver.close()
    
    return all_r


#%%
# =============================================================================
# Create search parameters using Pycountry
# =============================================================================

# List of countries we want to search through
country_list=['germany','china','united kingdom','spain','italy','singapore','hong kong',
               'us']

# country_list = ['hong kong','singapore']

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
        v = [term+ ' ' + x for x in v]
        cs[k] = v

    return cs        

search = search_creator(country_state,'covid')

#%%
# =============================================================================
# Saving tweets
# =============================================================================

results = {}
error = []

# Iterating through every country
for k,v in search.items():
    temp = [] #empty list to store current country responses
    for t in v:        
        # getting reponse for current state search and appending to list
        try:
            all_r =  search_twitter(t)
            temp = temp + all_r
        except:     
            fail = k +':'+t
            error.append(fail)

    
    # storing all state tweets to country
    results[k] = temp


#%%
# =============================================================================
# Saving results
# =============================================================================

for k,v in results.items():    
    k = k.replace(' ','_')
    with open(r'C:\Users\12shu\OneDrive - Kubrick Group\upskill\tweets_{}.txt'.format(k),'wb') as f:
        for t in v:                 
            f.write(str(t).encode('utf-8'))
            f.write('\n'.encode('utf-8'))            
            f.write('-----Line of Text------------'.encode('utf-8'))
            f.write('\n'.encode('utf-8'))
    f.close()

with open(r'C:\Users\12shu\OneDrive - Kubrick Group\upskill\error.txt','wb') as f:
    for v in error:
        f.write(str(v).encode('utf-8'))
        f.write('\n'.encode('utf-8'))            
        f.write('-----Line of Text------------'.encode('utf-8'))
        f.write('\n'.encode('utf-8'))
f.close()
    









    
    
    
        



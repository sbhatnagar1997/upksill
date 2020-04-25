"""
Author: Shubham Bhatnagar
Date Created: 25/04/2020

Purpose: Twitter API interaction script

"""

#%%
# =============================================================================
# Imports
# =============================================================================
import requests

#%%
# =============================================================================
# Creating connection to Twitter API
# =============================================================================

# =============================================================================
# url = "https://twitterbukativ1.p.rapidapi.com/search"
# 
# ck = 'YH3XF8MuFe0SZIprvqZsnjjC3'
# cks = 'SDayFNOWBS3HY34wKLlXLSX2DGwjOKrGmZfjPMqVWvMOCKHwRt'
# ak = '741422330-wh3NrXKkwicE5RhbEvsvbJvsORWLZuDhanYoAlZk'
# aks = 'yYzY8iXS5owbjlGMRiASxa34ZueTFIKwbJtWcYuZRMS6q'
# q = ''
# 
# payload = "consumerKey={}&query={}&accessTokenKey={}&consumerSecret={}&accessTokenSecret={}".format(ck,q,ak,cks,aks)
# headers = {
#     'x-rapidapi-host': "TwitterBukatiV1.p.rapidapi.com",
#     'x-rapidapi-key': "19a7424cc1mshe06401f1418a19bp1fd5d9jsn148caffdc24e",
#     'content-type': "application/x-www-form-urlencoded"
#     }
# 
# response = requests.request("POST", url, data=payload, headers=headers)
# 
# print(response.text)
# =============================================================================

api = 'https://api.twitter.com/1.1/search/tweets.json'

url = 'https://twitter.com/search?q=employment&src=typed_query'

ck = 'YH3XF8MuFe0SZIprvqZsnjjC3'
cks = 'SDayFNOWBS3HY34wKLlXLSX2DGwjOKrGmZfjPMqVWvMOCKHwRt'
ak = '741422330-wh3NrXKkwicE5RhbEvsvbJvsORWLZuDhanYoAlZk'
aks = 'yYzY8iXS5owbjlGMRiASxa34ZueTFIKwbJtWcYuZRMS6q'

search_url = api+ url[url.find('?')::]

payload = "consumerKey={}&accessTokenKey={}&consumerSecret={}&accessTokenSecret={}".format(ck,ak,cks,aks)
r = requests.get(search_url, data = payload)
"""
Author: Shubham Bhatnagar
Date Created: 01/05/2020

Purpose: Twitter interaction using webscraping
- https://towardsdatascience.com/web-scrape-twitter-by-python-selenium-part-1-b3e2db29051d
- Using the above tutorial.
"""

#%%
# =============================================================================
# Imports
# =============================================================================
import pycountry
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from sys import exit

from bs4 import BeautifulSoup as bs


#%%
# =============================================================================
# Selenium
# =============================================================================

def waiting_func(driver, by_variable,attribute):
    try:
        if by_variable.upper() == '8XPATH':
            WebDriverWait(driver,20).until(lambda x: x.find_element_by_xpath(attribute))
        else:
            WebDriverWait(driver,20).until(lambda x: x.find_element(by=by_variable, value=attribute))
            
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


def search_twitter(term):
    options = webdriver.ChromeOptions()
#    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Load twitter webpage
    driver.get(r'https://www.twitter.com/explore')

    # Waiting until the input box has appeared
    waiting_func(driver, 'xpath',
            r'//input[@data-testid="SearchBox_Search_Input"]')
 
    # Closing the agree Twitter's services box
    xpath = r'//div[@role="button"]'
    driver.find_element_by_xpath(xpath).send_keys(Keys.ENTER)
   
    # Searching for term in search box
    xpath = r'//input[@data-testid="SearchBox_Search_Input"]'
    driver.find_element_by_xpath(xpath).send_keys('{}'.format(term), Keys.ENTER)
    time.sleep(5)    


    # Scrolling through the page    n = 50
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
    
 

search_twitter('covid')

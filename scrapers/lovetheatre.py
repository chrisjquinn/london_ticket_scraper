#!/usr/bin/env python
# coding: utf-8
# CQ 27/02/2022

# Love theatre scraper
#Write out to `data/lovetheatre.csv`

## Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import time
import re
import os

DATA_PATH = os.getcwd()+'/data'
DRIVER_PATH = '/Users/'+os.getlogin()+'/Downloads/chromedriver'

driver = webdriver.Chrome(DRIVER_PATH)
print("Starting lovetheatre chromedriver...")


base_url = 'https://www.lovetheatre.com/'
driver.get(base_url)

columns = ['Name', 'Genre', 'Price', 'Venue', 'Run time', 'Start date', 'End date', 'URL']
events_df = pd.DataFrame(columns = columns)



def scrape_page(link):
    driver.get(base_url+link)
    
    urls = []
    venues = []
    prices = []
    names = []
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    blocks = soup.find_all('div', {'class':"post"})
    for block in blocks:
        url = block.find('a')['href']
        urls.append(url)
        
        venue = block.find('figure').figcaption.header.p.small.string
        if venue is None:
            venue = np.nan
        venues.append(venue)
        
        price = block.find('div',{'class': 'price'})
        if price is None:
            price = np.nan
        else:
            price = price.string.replace("£", "")
        prices.append(float(price))
        
        name = block.find('figcaption').h3.string
        names.append(name)
    
    working_df = pd.DataFrame(columns = columns)
    working_df['Name'] = names
    working_df['Venue'] = venues
    working_df['Genre'] = 'Play'
    working_df['Price'] = prices
    working_df['URL'] = urls
    
    return working_df




musicals_df = scrape_page('musicals/')
plays_df = scrape_page('plays/')
events_df = pd.concat([musicals_df, plays_df], axis=0)
events_df.to_csv(f'{DATA_PATH}/lovetheatre.csv')
driver.close()
print(f"livethetre chromedriver closed.")


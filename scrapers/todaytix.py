#!/usr/bin/env python
# coding: utf-8
# CQ 20/02/2022

# ## Ticket Scraper Prototype
# Aim: Successfully scrape 1 website for something with a 24h deal, cheaper than £20 etc. Then tell me on some sort of messaging app

# ## Imports

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

print("Starting todaytix chromedriver...")

driver.get('https://www.todaytix.com/london/category/all-shows')

time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/button').click()

time.sleep(1)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#Wait for the web elements to load
time.sleep(3)


def scrape_main_page():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    urls = []
    
    ## We want all the ones which are events, no other redirects to instagram or anything
    for block in soup.find_all('a'):
        link = block.get('href')
        urls.append(f'https://www.todaytix.com{link}')
    return urls

URLS = scrape_main_page()

events_df = pd.DataFrame(columns = ['Name', 'Genre', 'Price', 'Venue', 'Run time', 'Start date', 'End date', 'URL'], index=range(len(URLS)))

events_df['URL'] = URLS

time.sleep(2)
driver.find_element(By.ID, 'back-to-top').click()
driver.implicitly_wait(10)


def scrape_ticket_page(link, index):
    # Check the page returns
    try:
        response = requests.head(link, allow_redirects=True)
        
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        events_df['Name'][index] = soup.h1.string if soup.h1 else np.nan

        price = soup.find('div', string=re.compile(r'\bFrom £[0-9]{1,3}\b'))
        if price is None:
            price = np.nan
        else:
            price = price.string.replace("From £", "")
        events_df['Price'][index] = float(price)
        
        categories = ["Genre", "Venue", "Run time", "Start date", "End date"]
        
        blocks = soup.find_all('div', {'class': 'MuiGrid-grid-sm-6'})
        if blocks is None:
            for category in categories:
                events_df[category][index] = np.nan
        else: 
            for block in blocks:            
                if block.h5.string in categories:
                    events_df[block.h5.string][index] = block.p.string
        
        
    except requests.exceptions.TooManyRedirects:
        print(f"URL {link} exceeded redirects")
    except Exception as e:
        print(f"Other exception caught for URL: {link}")
        print(e)


for i in range(len(URLS)):
    scrape_ticket_page(URLS[i], i)


events_df.to_csv(f'{DATA_PATH}/todaytix.csv')


driver.close()
print("todaytix chromedriver closed.")


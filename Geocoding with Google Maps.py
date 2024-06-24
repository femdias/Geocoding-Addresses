# -*- coding: utf-8 -*-
"""
Created on Fri May 19 17:55:29 2023

@author: Users
"""

import selenium
import pandas as pd
import numpy as np
import time
import tqdm
import webdriver_manager
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os


# Setting working directory
os.chdir(r'C:\Users\femdi\Documents\GitHub\Geocoding')

# Importing addresses dataset 
df = pd.read_excel('Zipcodes_with_address.xlsx')


###############################################################################
# Creating "Search string" variable
###############################################################################

search_string = []
for i in range(len(df)):
    # List with 'pieces' of the address
    list_str = str(df.loc[i,'Street']).split(' - ')
    
    # Trying to select only numbers
    try: 
        # Replacing common substring in order to isolate only a number of the address
        nums = [int(s) for s in list_str[1].replace('de ', ',').replace('/', ',').replace('até ', ',').split(',') if s.isdigit()]
    
        # Final String 
        string = list_str[0] + ", " + str(nums[0] + 1) + ' - ' + str(df.loc[i,'Neighborhood']) + ", " + str(df.loc[i,'City'])
        search_string.append(string)
    except:
        string = list_str[0] + ' - ' + str(df.loc[i,'Neighborhood']) + ", " + str(df.loc[i,'City'])
        search_string.append(string)

df['Search_string'] = search_string


###############################################################################
# Using Seleminum and Google Maps to get coordinates of each place
###############################################################################

# Options for not getting popups
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized") # maximized window

# Initializing the WebDriver and openning URL
driver = webdriver.Chrome(options=chrome_options)

# Opening Google Maps site
driver.get("https://www.google.com.br/maps")


#Waiting until the website loads complety 
wait = WebDriverWait(driver,15).until(
     EC.presence_of_element_located((By.ID, "searchboxinput")))
    
# Importing subset
#df_results = pd.read_excel(r'Outputs\Hosp_CEPs_with_address_and_coordinates.xlsx')

# Loop
list_latitude = []
list_longitude = []
for i in tqdm.tqdm(range(len(df))):
        
    #Waiting until the website loads complety 
    wait = WebDriverWait(driver,20).until(
         EC.presence_of_element_located((By.CLASS_NAME, "searchboxinput")))
    
    # Finding the search bar
    search_bar = driver.find_element(By.CLASS_NAME,'searchboxinput')
    
    # Erasing what is written in the search bar
    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.DELETE)

    # Writing (the search string) in the searching bar
    search_bar.send_keys(df.loc[i, 'Search_string'] + "\n")


    ################## Change it for your Google's langeuage!!!!
    
    # If "correspondence is partial", click on the best correspondence
    try:
        correspondence = driver.find_element(By.CLASS_NAME,'Bt0TOd')
        if correspondence.text == 'Correspondência parcial':
            first_corresp = driver.find_element(By.CLASS_NAME, 'Nv2PK') 
            first_corresp.click()
    except:
        pass

    ''' Getting the geographic coordinates from Google Maps URL'''
    
    # Saving URL 
    link = driver.current_url
    
    # Checking if URL has coordinates, if not, waiting
    while True:
        if "@-" in link:
            break
        else:
            time.sleep(0.2)
            link = driver.current_url

    # Finding Coordinates
    coordenadas_before = link.split("@")[1].split(",")
    latitude_before = coordenadas_before[0]
    longitude_before = coordenadas_before[1]
    
    # Zooming 4x into the point (to get more precise coordinates)
    time.sleep(1)
    wait_zoom = WebDriverWait(driver,20).until(
         EC.presence_of_element_located((By.ID, "widget-zoom-in")))
    zoom_in = driver.find_element(By.ID, 'widget-zoom-in')
    zoom_in.click()
    zoom_in.click()
    zoom_in.click()
    zoom_in.click()
    

    # Finding coordinates again (and check if it is different from the previous)
    coords = driver.current_url.split("@")[1].split(",")
    latitude = coords[0]
    longitude = coords[1]
    
    # Testing if coordinates after the zoom are the same as before (we aim to get different coordinates, meaning that the zoom get a better locaization)
    while coords == coordenadas_before:
        time.sleep(0.2)
        coords = driver.current_url.split("@")[1].split(",")
        latitude = coords[0]
        longitude = coords[1]
        
    # Appending coordinates to list of them
    list_latitude.append(latitude)
    list_longitude.append(longitude)
    
    # Coming back to initial Google Maps page
    driver.get("https://www.google.com.br/maps")

driver.quit()

# Adding result list to dataframe
df_results = df.copy()
df_results['Latitude'] = list_latitude
df_results['Longitude'] = list_longitude

# Saving 
df_results.to_excel(r"Zipcodes_with_address_with_coord_Google_Maps.xlsx", index = False)


# stuff for the os
import os
import configparser
import io
import sys
import time, datetime

#dealing with the database
import sqlite3
import pandas as pd
from pandas import DataFrame

#parsing html/json/requests
import json
import requests
import lxml
from lxml import etree
from lxml import html

#useful utilties from selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#selenium things to run the webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from geopy.geocoders import Nominatim


class GenericScraper:

    def add_driver(self):
        opts = Options()
        if self.headless:
           opts.set_headless()
        driver = webdriver.Firefox(options=opts, executable_path=self.geckodriver_path)
        self.drivers.append(driver)


    def check_table(self, cur, tablename):
        """check to see if table exists"""
        query = ''' SELECT count(name) 
                    FROM sqlite_master 
                    WHERE type='table' 
                    AND name='%s' '''%tablename
        cur.execute(query)
        if cur.fetchone()[0] == 1:
            return True
        return False


    def get_censusdata(self,fields):
        """load formatted fields from census api"""
        api_query = "https://api.census.gov/data/2018/acs/acs5?&get=NAME"
        # print(fields)
        for field in fields:
            api_query = api_query + "," + field
        api_query = api_query + "&for=place:*&in=state:*"
        # print(api_query)
        #call the API and collect the response
        response = requests.get(api_query)
        #load the response into a JSON, ignoring the first element which is just field labels
        formattedResponse = json.loads(response.text)
        return formattedResponse


    def load_censusdata(self,db,censusfile):
        """add hardcoded census data to the database
        as a new table. drop table if already exists"""

        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        #check to see if table exists 
        if self.check_table(cur,"census"):
            cur.execute("drop table census") #if the table exists, drop it
        
        #get state data and save as a dataframe
        censusFielddata = pd.read_csv(censusfile)
        census_codes = list(censusFielddata["census_code"])
        censusdata = self.get_censusdata(census_codes)

        fieldnames = list(censusFielddata["column"]) #these are the names you should use
        fieldnames.insert(0, 'NAME')  
        fieldnames.extend(['state', 'place'])

        #create a query that inserts into the new table
        create_census = "CREATE TABLE census (" + " VARCHAR(250),".join(fieldnames) + " VARCHAR(250))" 

        cur.execute(create_census)

        st = pd.DataFrame(columns=fieldnames, data=censusdata)
        df = st.iloc[1:]  # omit reading the census codes
        cols = ",".join([str(i) for i in fieldnames])
        for i,row in df.iterrows():
            sql = "INSERT INTO census (" + cols + ") VALUES (" + "?, "*(len(row)-1) + "?)"
            cur.execute(sql, tuple(row))
            conn.commit()

        #commit changes to db
        conn.commit()


    def load_statedata(self,db,statefile):
        """add hardcoded state data to the database
        as a new table"""
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        #check to see if table exists
        if self.check_table(cur,"states"):
            cur.execute("drop table states") #if the table exists, drop it
        #get state data and save as a dataframe
        statedata = pd.read_csv(statefile)

        #create a query that creates a table with the columns names
        fieldnames = list(statedata.columns) #these are the names you should use

        #create a query that inserts into the new table
        create_states = "CREATE TABLE states (" + " VARCHAR(250),".join(fieldnames) + " VARCHAR(250))" 
        
        cur.execute(create_states)

        cols = ",".join([str(i) for i in fieldnames])
        for i,row in statedata.iterrows():
            sql = "INSERT INTO states (" + cols + ") VALUES (" + "?, "*(len(row)-1) + "?)"
            cur.execute(sql, tuple(row))
            conn.commit()


    def entry_create(self,db):
        """run the sql file to create the db"""
        f = open("db/db_create.sql","r")
        sql = f.read()
        conn = sqlite3.connect(db) #create the db
        cur = conn.cursor()
        cur.executescript(sql)
        conn.commit()


    def db_create(self,db):
        censusfile = "db/columns.csv"
        statefile = "db/states.csv"
        if not os.path.isfile(db):
            self.entry_create(db)
        self.load_statedata(db,statefile)
        self.load_censusdata(db,censusfile)


    def __init__(self, url="", store_directory ="", store="", config_file="config.ini",
                    headless=False, num_drivers=1):
        """initialize the scraping class"""

        #read config file as a n arguement
        for i, arg in enumerate(sys.argv):
            if i==1:
                config_file = str(arg)

        #get info from the config file
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(config_file)

        #file paths
        self.db = config.get('Paths','db_path')
        self.geckodriver_path = config.get('Paths','geckodriver_path')

        # home depot or lowes
        self.base_url = url
        self.store_directory = store_directory
        self.store = store

        #info about the scrape
        self.headless = headless  #do windows open that show the scrape in progress
        self.drivers = []
        self.num_drivers = num_drivers

        #create the database
        self.db_create(self.db)

        #initialize web browsers called 'drivers' to do the scrape
        for i in range(self.num_drivers):
            print("------ initializing %s"%self.store)
            self.add_driver()
        
        
    def get_driver(self):
        return self.drivers[-1]


    def end_scrape(self):
        for driver in self.drivers:
            driver.quit()


    def get_obs(self):
        return {"address":None, "city":None,
        "state":None, "zipcode":None, "url":self.base_url,
        "time":datetime.datetime.now().timestamp()}


    def save_obs(self,obs):
        """insert observation saved as a dictionary into the database
        keys must match db_create.sql"""

        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        query_pt1 = " INSERT INTO entry (store"
        query_pt2 = " VALUES ('%s'"%self.store

        for key in obs.keys():
            
            if obs[key] is not None:
                #print(key,obs[key])
                query_pt1 = query_pt1 + "," + key
                key_value = str(obs[key]).replace('\\','').replace("'","")
                query_pt2 = query_pt2 + ",'%s'"%key_value

        query_pt1 = query_pt1 + ")"
        query_pt2 = query_pt2 + ")"

        try:
            c.execute(query_pt1 + query_pt2)
        except Exception as err:
            print(query_pt1 + query_pt2)
            print(err)

        conn.commit()


    def search_xpath(self,tree,query):
        """hacky way to parse xpath takes an etree as an arguement"""
        return tree.xpath("//*[contains(text(), '%s') or @*[contains(., '%s')]]"%(query,query))


if __name__ == "__main__":
    scrap = GenericScraper(num_drivers=0)


# for command line:
# cd C:\Users\himan\LoweHomeDepot\
# python scraper.py C:\Users\himan\LoweHomeDepot\config.ini 
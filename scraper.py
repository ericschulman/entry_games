# stuff for the os
import os
import configparser
import io
import sys
import time, datetime

#dealing with the database
import sqlite3

#parsing html
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


    def db_create(self,db):
        """run the sql file to create the db"""
        f = open("db/db_create.sql","r")
        sql = f.read()
        if (os.path.isfile(db) ):
            os.remove(db_name)
        con = sqlite3.connect(db) #create the db
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()



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

        #initialize web browsers called 'drivers' to do the scrape
        for i in range(self.num_drivers):
            print("------ initializing %s"%self.store)
            self.add_driver()
        
        #create the database if it is not there
        if not os.path.isfile(self.db) :
            self.db_create(self.db)


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



#if __name__ == "__main__":

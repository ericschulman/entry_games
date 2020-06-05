# stuff for the os
import os
import configparser
import io

#dealing with the database
import sqlite3

#parsing html
import lxml
from lxml import etree
from lxml import html

#useful utilties from selenium
from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support import expected_conditions
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
#from selenium.common.exceptions import TimeoutException


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



    def __init__(self, url="", store="", config_file="config.ini",
                    headless=False, num_drivers=1):
        """initialize the scraping class"""

        config = configparser.ConfigParser(allow_no_value=True)
        config.read(config_file)

        #file paths
        self.db = config.get('Paths','db_path')
        self.geckodriver_path = config.get('Paths','geckodriver_path')

        # home depot or lowes
        self.base_url = url
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


    def end_scrape(self):
        for driver in self.drivers:
            driver.quit()


    def search_xpath(self,tree,query):
        """hacky way to parse xpath takes an etree as an arguement"""
        return tree.xpath("//*[contains(text(), '%s') or @*[contains(., '%s')]]"%(query,query))



if __name__ == "__main__":
    print("hello world")
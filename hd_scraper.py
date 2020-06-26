from scraper import *

class HomeDepotScraper(GenericScraper):

    def __init__(self,*args, **kwargs):
        kwargs["url"] = "https://www.homedepot.com/"
        kwargs["store_directory"] = "StoreFinder/storeDirectory"
        kwargs["store"] = "HD"
        super(HomeDepotScraper, self).__init__(*args, **kwargs)



    def click_state_links(self):
        """go through each of the states and click the link"""
        for i in range(1,55):
            driver = self.get_driver() #get a webdriver from the scraper
        

            #example 2- find the link using html tags/xpath queries
            driver.get(self.base_url + self.store_directory) #load the store directory, by combining it with the base url


            #get the html element - try to under stand what this line is doing
            state_xpath_query = '(//*[@class="stateList__item"])[' + str(i) + ']' #xpath query to the first state on the page
            state_element = driver.find_element(By.XPATH, state_xpath_query) 
            #to fully understand the previous line, you will have to understand how I am querying the webpage
            #what does [1] do in line 23?
            #what does * do in line 23?
            #what does @class do in line 23?

            state_html = state_element.get_attribute('innerHTML') #get the html text from the xpath element
            state_tree = etree.fromstring(state_html) #parse it as a tree
            driver.get(self.base_url + state_tree.attrib["href"]) #get the href attribute and go to that page


    def get_obs(self):
        self.click_state_links()
        return super(HomeDepotScraper, self).get_obs()


if __name__ == "__main__":
    #you will need to change the gecko_driver path to run your own scrape
    scrap = HomeDepotScraper()
    obs = scrap.get_obs()
    scrap.save_obs(obs)
    scrap.end_scrape()
from scraper import *

class HomeDepotScraper(GenericScraper):

    def __init__(self,*args, **kwargs):
        kwargs["url"] = "https://www.homedepot.com/"
        kwargs["store_directory"] = "StoreFinder/storeDirectory"
        kwargs["store"] = "HD"
        super(HomeDepotScraper, self).__init__(*args, **kwargs)


    def collect_data(self, driver):
        """for each page, collect the relevant information about stores and save to the data
        base"""
        for store in driver.find_elements(By.XPATH, '//*[@class = "storeList__item"]'):
            if store.find_elements_by_partial_link_text('Area Services'):
                break
            store_detail = store.find_element_by_class_name("storeList__details")
            store_details = store_detail.get_attribute('innerText')
            store_address = store_details.split('\n')[0]
            store_city_list = store_details.split('\n')[1].split(' ')[:-2]
            store_city = ' '.join(store_city_list)
            store_state = store_details.split('\n')[1].split(' ')[-2]
            store_zipcode = store_details.split('\n')[1].split(' ')[-1]

            new_obs = super(HomeDepotScraper, self).get_obs()
            new_obs['address'] = store_address
            new_obs['city'] = store_city
            new_obs['state'] = store_state
            new_obs['zipcode'] = store_zipcode
            self.save_obs(new_obs) # save the observation to the database


    def get_obs(self):
        """go through each of the states and click the link"""
        driver = self.get_driver()
        driver.get(self.base_url + self.store_directory)
        state_elements = driver.find_elements(By.XPATH, "//*[@class='stateList__item']")
        href_list = []
        for state_element in state_elements:
            state_html = state_element.find_element_by_css_selector('a')
            state_url = state_html.get_attribute('href')
            while state_url not in href_list:
                href_list.append(state_url)
        for href in href_list:
            driver.get(href) 
            self.collect_data(driver)
            

        
if __name__ == "__main__":
    #you will need to change the gecko_driver path to run your own scrape
    scrap = HomeDepotScraper()
    scrap.get_obs()
    scrap.end_scrape()
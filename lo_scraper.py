from scraper import *

class LowesScraper(GenericScraper):

    def __init__(self,*args, **kwargs):
        kwargs["url"] = "https://www.lowes.com/"
        kwargs["store_directory"] = "Lowes-Stores"
        kwargs["store"] = "LOW"
        super(LowesScraper, self).__init__(*args, **kwargs)


    def geolocate_cities(self,store_city,store_state,num_stores):
        # geolocator
        geolocator = Nominatim(user_agent="user",timeout=10)
        geocode_string = "Lowe's, " + store_city + ", " + store_state
        locations = geolocator.geocode(geocode_string, exactly_one=False)
        if store_city == "Birmingham":
            print(locations)


        if locations is not None:
            for x in locations:
                city_address = (x[0]).split(', ')[1]
                city_zip = (x[0]).split(', ')[-2]

                new_obs = super(LowesScraper, self).get_obs()
                new_obs['address'] = city_address
                new_obs['zipcode'] = city_zip 
                new_obs['city'] = store_city
                new_obs['state'] = store_state
                self.save_obs(new_obs) # save the observation to the database
        else:
            locations = []
            print(geocode_string)

        for i in range( max(num_stores - len(locations), 0) ):
            new_obs = super(LowesScraper, self).get_obs()
            new_obs['city'] = store_city
            new_obs['state'] = store_state
            self.save_obs(new_obs) # save the observation to the database


    def collect_data(self, driver):
        """ for each page, collect the relevant information about stores and save to the data
        base """
        
        store_state = ''
        for store_state_element in driver.find_elements(By.XPATH, '//*[@class = "grid-100 v-spacing-large"]'):
            store_state_css = store_state_element.find_element_by_css_selector('h1')
            store_state = store_state_css.get_attribute('innerText')
            break

        cities = {} #save all cities and number of cities first
        for store in driver.find_elements(By.XPATH, '//*[@class = "v-spacing-small"]'):
            store_css = store.find_element_by_css_selector('span')
            store_city_text = store_css.get_attribute('innerText')
            store_city = store_city_text.replace(u'\xa0', u'').strip(',')

            if store_city in cities.keys():
                cities[store_city] = cities[store_city] + 1
            else:
                cities[store_city] = 1
        
        #geolocate cities next
        for store_city in cities.keys():
            num_stores = cities[store_city]
            self.geolocate_cities(store_city,store_state,num_stores)


    def get_obs(self):
        """go through each of the states and click the link"""
        driver = self.get_driver()
        driver.get(self.base_url + self.store_directory)
        state_item = driver.find_elements(By.XPATH, 
            "//div[@id='mainContent']//div[@class='grid-33 tablet-grid-33 mobile-grid-100']//li[@role='listitem']")
        href_list = []
        for item in state_item:
            state_html = item.find_element_by_css_selector('a')
            state_url = state_html.get_attribute('href')
            if ('Lowes-Stores' in state_url) and (state_url not in href_list):
                href_list.append(state_url)
        for href in href_list:
            self.add_driver()
            new_driver = self.get_driver()
            new_driver.get(href)
            self.collect_data(new_driver)
            new_driver.close()


if __name__ == "__main__":
    scrap = LowesScraper()
    scrap.get_obs()
    scrap.end_scrape()


# for command line:
# cd C:\Users\himan\LoweHomeDepot\
# python lo_scraper.py C:\Users\himan\LoweHomeDepot\config.ini 
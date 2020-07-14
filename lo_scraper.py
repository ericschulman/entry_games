from scraper import *


class LowesScraper(GenericScraper):

    def __init__(self,*args, **kwargs):
        kwargs["url"] = "https://www.lowes.com/"
        kwargs["store_directory"] = "Lowes-Stores"
        kwargs["store"] = "LOW"
        super(LowesScraper, self).__init__(*args, **kwargs)


    def collect_data(self, driver):
        """ for each page, collect the relevant information about stores and save to the data
        base """
        for store in driver.find_elements(By.XPATH, '//*[@class = "v-spacing-small"]'):
            store_css = store.find_element_by_css_selector('span')
            store_city_text = store_css.get_attribute('innerText')
            store_city = store_city_text.replace(u'\xa0', u'').strip(',')

            new_obs = super(LowesScraper, self).get_obs()
            new_obs['city'] = store_city
            
            # self.save_obs(new_obs) # save the observation to the database

        return new_obs 


    def get_obs(self):
        """go through each of the states and click the link"""
        driver = self.get_driver()
        driver.get(self.base_url + self.store_directory)
        state_element = driver.find_element(By.XPATH, "//div[@class='grid-33 tablet-grid-33 mobile-grid-100']")
        state_list = state_element.find_elements(By.XPATH, "//ul[@class='list unstyled']")
        href_list = []
        for elem in state_list:
            state_item = elem.find_elements(By.XPATH, "//*[@role='listitem']")
            for item in state_item:
                state_html = item.find_element_by_css_selector('a')
                state_url = state_html.get_attribute('href')
                if 'Lowes-Stores' in state_url:
                    while state_url not in href_list:
                        href_list.append(state_url)
        for href in href_list:
            driver.get(href)
            # self.collect_data(driver)


if __name__ == "__main__":
    scrap = LowesScraper()
    scrap.get_obs()
    scrap.end_scrape()
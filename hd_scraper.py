from scraper import *

class HomeDepotScraper(GenericScraper):

    def __init__(self,*args, **kwargs):
        kwargs["url"] = "https://www.homedepot.com/StoreFinder/storeDirectory"
        kwargs["store"] = "HD"
        super(HomeDepotScraper, self).__init__(*args, **kwargs)

if __name__ == "__main__":
	#you will need to change the gecko_driver path to run your own scrape
    scrap = HomeDepotScraper()
    scrap = HomeDepotScraper(config_file="C:\\Users\\himan\\LoweHomeDepot\\config.ini")
    scrap.end_scrape()
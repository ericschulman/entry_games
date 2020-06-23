from scraper import *


class LowesScraper(GenericScraper):

    def __init__(self,*args, **kwargs):
        kwargs["url"] = "https://www.lowes.com/"
        kwargs["store_directory"] = "Lowes-Stores"
        kwargs["store"] = "LOW"
        super(LowesScraper, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    
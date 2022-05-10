# Overview
Scrape lowes and home depot entry decisions. The scrapped data was then used to estimate an empirical entry game model similar to the model studied by [Bresnahan and Reiss](https://www.jstor.org/stable/2937655). 

# Scraper

This code was used to scrape Lowe's and Home Depot's websites in summer 2020 for store locations. The template for the scraper is in `scraper.py`. `hd_scraper.py` and `lo_scraper.py` extend this template and modify it for each of the specific sites. The scrapers dump the data in `db/entry.db`. `db/db_create.sql` will initialize this database with the correct schema.

## Dependecies

1. `selenium` - This program opens up a browser window and lets you input commands using python. I installed using `anacondas` but `pip` should work. There's a helpful browser extension you can play with that "automatically" writes code
https://www.selenium.dev/selenium-ide/

2. `geckodriver` - This program provides the browser for selenium to issue commands to. I also installed using anacondas

3. `sqlite` I have found the following graphical shell helpful, https://sqlitebrowser.org/

## Configuring the repo

In order to run the program you will need to create your own `config.ini` in the parent directory. I have included `config_example.ini` to demonstrate what's involved. Right now, there are 2 different paths that need to be specified (1) the database (2) the location where `geckodriver` is installed.

-------

# Empirical model

## Overview

I study Lowe's and Home Depot's entry decisions across the U.S. similar to [Aradillas Lopez (2011)](https://onlinelibrary.wiley.com/doi/abs/10.3982/QE74). I consider different theoretical specifications for the model, based on information structure. I consider complete and incomplete information. I select between them using the Vuong test and the bootstrap. The code for this is in the `estimation` folder. 

I estimate two models, both of which are completely parametric, based on the 2x2 entry game starting in [Bresnahan and Reiss](https://www.jstor.org/stable/2937655). The models differ based on information structure, i.e. complete information and incomplete information.  In the game of complete information, firms share information that the researcher does not have access to. Thus, complete information should introduce coordination between the two firms' decisions. I test to see which version of the model is closer to the data.


### Modules

* `selection_tests.py`/`selection_tests_copula.py` are the model tests designed by [my job market paper](https://drive.google.com/file/d/14FdLzfvJzOyyH0F6itTg2TeE7dgiF9Jd/view). 

* `selection_tests.py` also contains the for estimating the entry game. It is implmeneted using `statsmodels`  class called [`GenericLikelihoodModel`](https://www.statsmodels.org/dev/dev/generated/statsmodels.base.model.GenericLikelihoodModel.html). The complete information game is called `NashLogit`. The incomplete information game is called `BayesNashLogit`. In the complete information model, firms perceive actions as deterministic.  There is more coordination; firms have information that the researcher does not.  As a result, the complete information model predicts more competition at the same levels of population compared to incomplete information.  The incomplete information model predicts more competition at the same levels of population. In incomplete information, decisions are independent, conditional on covariates.

* `shi_test.py` Python implementation of the test designed by by [Shi (2015)](https://onlinelibrary.wiley.com/doi/abs/10.3982/QE382).
## Overview of estimation

This repository contains code for estimating a game of complete information and a game of incomplete information. This repository collects a cross-section of data of Lowe's and Home Depot's entry decisions across the United States.  As a market definition, I consider all census designated places in the 2018 census data. The outcome variable is the entry decisions of Lowe's and Home Depot for a given city. I consider the following covariates from the 2018 American community survey (ACS).


## Data

The `data` folder contains the files necessary for preprocessing and running the estimatin routine.

* Population: population in the i-th market according the ACS data.
* Income per capita: The median income per capita according to ACS data.
* Distance from Distribution Center: This would be the distance to the nearest Lowe's or Home Depot distribution center.

The following datafiles are included:

* `distr.csv` - this is the location of the distribution centers without geolocations
* `entry.csv` - The actual locations for Lowe's and Home Depot.
* `warehouse_loc.csv` - Geolocated distribution centers.
* `entry_loc.csv` - Distance between each location and the HQ. 
* `entry_locv2.csv` - Warehouse locations merged with entry locations
* `entry_loc3_w_filter.csv` - Tries to change geography of the dataset from CDPs to CBSAs


## Preprocessing files

* `scrape_CBSA` calls the census api to get the CBSA data.
* `hq_dist.ipynb` determines the distance between each row and the HQ. It creates `entry_loc.csv`.
* `warehouses.ipynb` merges the warehouse data with the scrape. It creates `entry_loc2.csv`. It also creates the geographic indicator variables. `hq_dist.ipynb` must be run before.
* `CDP_CBSA` tries to change the census geography of the dataset from CDPs to CBSAs `warehouse.ipynb` should be run before. 
* `merged_entry.csv` is the result of a sql query in `summary_stats.sql`.

## Estimation files

* `model_selection` folder contains `model_fit.ipynb`. This contains the model selection test. Different versions correspond to different geographies of the census data.
* The folder `reduced_form` regression estimates. There are various versions of `separate_estimate.ipynb` which looks at reduced form estimates of linear regression on entry decisions. Different versions correspond to different geographies of the census data.
* `visualizations.ipynb`
* `incomplete_info` and `complete_info` are folders dedicated to developing each model respectively. There is a work in progress version of the model with a copula. `data.ipynb` is used to generate Monte Carlo data where the parameters are known.

-------

### Complete Information Results

NashLogit combinations that work with tolerance:
1. income_2 
2. population_2
3. under44_1_2
4. under44_2_2
5. under44_3_2
6. older65_1_2
7. older65_2_2 
8. income_2, under44_1_2
9. income_2, older65_1_2
10. income_2, older65_2_2
11. under44_1_2, older65_1_2
12. under44_1_2, older65_2_2
13. under44_1_2, under44_3_2, older65_1_2
14. income_2, under44_3_2, older65_2_2

- Population doesn't work with anything else.

###  Incomplete Information Results

BayesNashLogit combinations that work with tolerance:
1. income_2, population_2
2. income_2, under44_1_2
3. income_2, under44_2_2
4. income_2, under44_3_2
5. income_2, under44_1_2, under44_2_2
6. income_2, under44_1_2, under44_3_2
7. income_2, under44_2_2, under44_3_2
8. income_2, population_2, older65_2_2

-------

### Comparing coefficients:
HD:
NashLogit:
1. Income = -1.0573
2. Population = 1.1026
BayesNashLogit: 
1. Income = -0.2697
2. Population = 0.2743
OLS:
1. Income: 0.0186
2. Population: 0.0548

LO:
NashLogit:
1. Income = 3.9061
2. Population = 0.0097
BayesNashLogit: 
1. Income = 2.1167
2. Population = -0.2629
OLS:
1. Income: 0.0025
2. Population: 0.0527

Observations:
* NashLogit produces nans even with set tolerance.
* Income values are negative for NashLogit/BayesNashLogit in HD.
* Population only negative for BayesNashLogit in LO.
* All coefficients in OLS are positive, and have smaller/comparable values.

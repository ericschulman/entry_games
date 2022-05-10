## Complete->Estimate.py

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

## Incomplete->Estimate.py

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

# Comparing coefficients:
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
# NashLogit produces nans even with set tolerance.
# Income values are negative for NashLogit/BayesNashLogit in HD.
# Population only negative for BayesNashLogit in LO.
# All coefficients in OLS are positive, and have smaller/comparable values.
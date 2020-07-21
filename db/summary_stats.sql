#figure out the average number of stores per state
with obs_per_state as (select state, count(*) as num_obs from entry group by state)

select avg(num_obs) from obs_per_state

#calculate the variance of number of stores
with obs_per_state as (select state, count(*) as num_obs from entry group by state)

select avg(num_obs*num_obs) - avg(num_obs)*avg(num_obs) from obs_per_state



#1. count the number of lowe's in each city, but remove duplicate adresses/zipcode combos

#2. count the number of homedepots in each city, but remove duplicate adress/zipcode combos

#3. join the previous two queries at the city level


#figure out the average number of stores per state
with obs_per_state as (select state, count(*) as num_obs from entry group by state)

select avg(num_obs) from obs_per_state

#calculate the variance of number of stores
with obs_per_state as (select state, count(*) as num_obs from entry group by state)

select avg(num_obs*num_obs) - avg(num_obs)*avg(num_obs) from obs_per_state

#join hd and lowes at the city level
WITH hd_no_dups AS (SELECT * FROM entry WHERE store='HD' 
	GROUP BY address,zipcode), 

lo_no_dups AS (SELECT * FROM entry WHERE store='LOW'
	GROUP BY address,zipcode),

hd AS (SELECT count(*) as HD, city, state 
	FROM hd_no_dups group by city, state order by state,city), 

lo AS (SELECT count(*) as LO, city, state  
	FROM lo_no_dups group by city, state order by state,city)

SELECT * FROM hd
LEFT JOIN lo ON hd.city = lo.city


#select Montgomery observations
select * from entry where  INSTR(city, "Montgomery") >=1


# add view that joins entry with states
CREATE VIEW joined AS
SELECT entry.address, entry.city, entry.store, entry.time, entry.url, entry.zipcode, 
states.STATE, states.STATENS, states.STATE_NAME, states.STUSAB
FROM entry, states
WHERE entry.state = states.STATE_NAME
OR entry.state = states.STUSAB

# join on state as well
WITH hd_no_dups AS (SELECT * FROM joined WHERE store='HD' 
	GROUP BY address,zipcode), 

lo_no_dups AS (SELECT * FROM joined WHERE store='LOW'
	GROUP BY address,zipcode),

hd AS (SELECT count(*) as HD, city, state 
	FROM hd_no_dups group by city, state order by state,city), 

lo AS (SELECT count(*) as LO, city, state  
	FROM lo_no_dups group by city, state order by state,city)

SELECT * FROM hd
LEFT JOIN lo ON hd.city = lo.city
AND hd.state = lo.state

# merge census data
SELECT * FROM entry
LEFT JOIN census ON instr(census.name, entry.city) = entry.city
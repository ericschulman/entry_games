#figure out the average number of stores per state
with obs_per_state as (select state, count(*) as num_obs from entry group by state)

select avg(num_obs) from obs_per_state

#calculate the variance of number of stores
with obs_per_state as (select state, count(*) as num_obs from entry group by state)

select avg(num_obs*num_obs) - avg(num_obs)*avg(num_obs) from obs_per_state


# final
with entry_states AS (SELECT entry.address, entry.city, entry.store, entry.time, entry.url, entry.zipcode, 
states.STATE, states.STATENS, states.STATE_NAME, states.STUSAB
FROM entry, states
WHERE entry.state = states.STATE_NAME
OR entry.state = states.STUSAB), 

census_desc as (SELECT * FROM census ORDER BY population DESC),

census_join AS (SELECT * FROM entry_states
LEFT JOIN census_desc AS census ON instr(census.name, entry_states.city) >= 1 
and instr(census.name, entry_states.STATE_NAME) >= 1
GROUP BY address
ORDER BY population DESC),

hd_no_dups AS (SELECT * FROM entry_states WHERE store='HD' 
	GROUP BY address,zipcode), 

lo_no_dups AS (SELECT * FROM entry_states WHERE store='LOW'
	GROUP BY address,zipcode),

hd AS (SELECT count(*) as HD, city, state 
	FROM hd_no_dups group by city, state order by state,city), 

lo AS (SELECT count(*) as LO, city, state  
	FROM lo_no_dups group by city, state order by state,city)
	
SELECT * FROM hd
LEFT JOIN lo ON hd.city = lo.city
AND hd.state = lo.state
LEFT JOIN census_join ON hd.city = census_join.city
AND hd.state = census_join.STATE 
GROUP BY hd.city, hd.state
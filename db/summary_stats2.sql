with entry_states AS (SELECT entry.address, entry.city, entry.store, entry.time, entry.url, entry.zipcode, 
CAST(states.STATE as INTEGER) as state, states.STATENS, states.STATE_NAME, states.STUSAB
FROM entry, states
WHERE entry.state = states.STATE_NAME
OR entry.state = states.STUSAB), 

census_int as (select substr(NAME,0, instr(NAME, ',')) as city, 
CAST(place as INTEGER) as place, CAST(state as INTEGER) as state, CAST(population as INTEGER) as population, CAST(income_per_capita as INTEGER) as income_per_capita,
CAST(under44_1 as INTEGER) AS under44_1, CAST(under44_2 as INTEGER) AS under44_2,
CAST(under44_3 as INTEGER) AS under44_3, CAST(older65_1 as INTEGER) AS older65_1,
CAST(older_65_2 as INTEGER) AS older_65_2
 from census),
	
census_asc as (SELECT * FROM census_int WHERE income_per_capita >= 3012 and population >= 106 ORDER BY population ASC),

census_join AS (SELECT census_asc.city,entry_states.state,entry_states.store  FROM entry_states
LEFT JOIN census_asc ON  census_asc.state = entry_states.state
and instr(census_asc.city,entry_states.city) >= 1
GROUP BY address,entry_states.city, STATE_NAME
ORDER BY entry_states.STATE_NAME,entry_states.city ASC),

entry_cities AS (SELECT city, state, sum(store = 'HD') as HD, sum(store='LOW') as LOW 
FROM census_join GROUP BY city, state)

select census_asc.city as city, census_asc.state as state, ifnull(HD, 0) as HD, ifnull(LOW, 0) as LOW, population, income_per_capita,
under44_1, under44_2, under44_3, older65_1, older_65_2
FROM census_asc
LEFT JOIN entry_cities ON entry_cities.city = census_asc.city AND
entry_cities.state = census_asc.state;


import sqlite3
import os
from datetime import datetime as dt

# https://discuss.codecademy.com/t/data-science-independent-project-5-analyze-airfare-data/419949

connection = sqlite3.connect('db.db')
crsr = connection.cursor()

def q(statement):
	return crsr.execute(statement).fetchall()

def basic():
	# Exploration: Familiarize yourself with the dataset.

	# What range of years are represented in the data?

	years = q("""
		SELECT DISTINCT Year
		FROM airfare_data
		ORDER BY Year ASC
	""")

	# What are the shortest and longest-distanced flights, and between which 2 cities are they?
	# Note: When we imported the data from a CSV file, all fields are treated as a string. Make sure to convert the value field into a numeric type if you will be ordering by that field. See here 25 for a hint.

	shortest_longest_flights = q("""

		WITH main (city1, city2, miles) AS (
				SELECT city1, city2, CAST(nsmiles AS INT)
				FROM airfare_data
			),
			min_max AS (
				SELECT min(miles) AS min, max(miles) AS max
				FROM main
			),
			min_cities AS (
				SELECT city1, city2, CAST(nsmiles AS INT) AS miles
				FROM airfare_data
				WHERE miles == (SELECT min FROM min_max)
					OR miles == (SELECT max FROM min_max)
			)

		SELECT * FROM min_cities
		GROUP BY miles

	""")

	# How many distinct cities are represented in the data (regardless of whether it is the source or destination)?
	# Hint: We can use UNION to help fetch data from both the city1 and city2 columns. Note the distinction between UNION and UNION ALL.
	# >> The UNION command combines the result set of two or more SELECT statements (only distinct values)
	# >> The UNION ALL command combines the result set of two or more SELECT statements (allows duplicate values)

	distinct_cities = q("""
		WITH cities AS (
			SELECT city1 FROM airfare_data
			UNION
			SELECT city2 FROM airfare_data
		)
		SELECT count(*) FROM cities
	""")

	# Analysis: Further explore and analyze the data.
	# Which airline appear most frequently as the carrier with the lowest fare (ie. carrier_low)?

	lowest_airfare_carrier = q("""

		WITH lowest_airfare AS (
				SELECT carrier_low, CAST(fare_low AS REAL) AS fare
				FROM airfare_data
					WHERE fare_low != ''
			)

		SELECT DISTINCT carrier_low
		FROM airfare_data
			WHERE CAST(fare_low AS REAL) == (SELECT min(fare) FROM lowest_airfare)

	""")

	# How about the airline with the largest market share (ie. carrier_lg)?

	largest_market_share = q("""

		WITH largest_ms AS (
				SELECT carrier_lg, CAST(large_ms AS REAL) AS ms
				FROM airfare_data
			)

		SELECT DISTINCT carrier_lg
		FROM airfare_data
			WHERE CAST(large_ms AS REAL) == (SELECT max(ms) FROM largest_ms)

	""")

	# How many instances are there where the carrier with the largest market share is not the carrier with the lowest fare? What is the average difference in fare?

	instances = q("""

		WITH
			main (carrier_low, fare, carrier_lg, ms) AS (
				SELECT carrier_low, CAST(fare_low AS REAL), carrier_lg, CAST(large_ms AS REAL)
				FROM airfare_data
					WHERE fare_low != ''
				),
			min_fare AS (
				SELECT DISTINCT carrier_low
				FROM main
					WHERE fare == (SELECT min(fare) FROM main)
				),
			max_mash AS (
				SELECT DISTINCT carrier_lg
				FROM main
					WHERE ms == (SELECT max(ms) AS max FROM main)
				)

			SELECT carrier_lg
			FROM max_mash
			JOIN min_fare
				ON carrier_lg != carrier_low

	""")

	# print(lowest_airfare_carrier)
	# print(largest_market_share)
	# print(instances)

	average_difference_in_fare = q("""

		WITH diff_to_avg (diff) AS (
			SELECT
				(CAST(fare AS INT) - (SELECT avg(CAST(fare AS INT)) FROM airfare_data))
			FROM airfare_data
			)

		SELECT avg(diff)
		FROM diff_to_avg

	""")

def intermediate():
	# What is the percent change 3 in average fare from 2007 to 2017 by flight? How about from 1997 to 2017?
		# Hint: We can use the WITH clause to create temporary tables containing the airfares, then join them together to compare the change over time.

	change_in_avg_fare = q("""

		WITH avg_annual (year, avg_fare) AS (
			SELECT CAST(year AS INT), avg(CAST(fare AS REAL))
			FROM airfare_data
			GROUP BY year
			)

			SELECT sum(avg_fare)
			FROM avg_annual
			WHERE avg_annual.year BETWEEN {0} AND {1}

	""".format(1997, 2017))

	# How would you describe the overall trend in airfares from 1997 to 2017, as compared 2007 to 2017?

def advanced():
	pass
	# What is the average fare for each quarter? Which quarter of the year has the highest overall average fare? lowest?
		# Note: Not all flights (ie. each city-pair route) have data from all 4 quarters - which may skew the average. Let’s try considering only flights that have data available for all 4 quarters.

	# Considering only the flights that have data available on all 4 quarters of the year, which quarter has the highest overall average fare? lowest? Try breaking it down by year as well.
		# Hint: To consider only flights that have data available for all 4 quarters, we could join the table with itself - each of those tables should be filtered to have data from one quarter.

# basic()
intermediate()
# advanced()
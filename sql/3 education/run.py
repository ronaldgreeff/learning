import sqlite3
import os
from datetime import datetime as dt

# https://discuss.codecademy.com/t/data-science-independent-project-3-education-census-data/419947

connection = sqlite3.connect('db.db')
crsr = connection.cursor()

def q(statement):
	return crsr.execute(statement).fetchall()


def basic():
	# How many public high schools are in each zip code? in each state?
	public_schools_per_zip_code = q("""
		SELECT zip_code, count(school_id)
		FROM public_hs_data
		GROUP BY zip_code
		ORDER BY count(school_id) DESC
	""")

	public_schools_per_state = q("""
		SELECT state_code, count(school_id)
		FROM public_hs_data
		GROUP BY state_code
		ORDER BY count(school_id) DESC
	""")

	# The locale_code column in the high school data corresponds to various levels of urbanization as listed below.
	# Use the CASE statement to display the corresponding locale_text and locale_size in your query result.
	# Hint: Try taking a look at using the substr() function to help look at each part of the locale_code for determining locale_text and locale_size.

	# NOTES:
	# CASE is one of the SELECT statement's field names - so include a comma (SELECT school_id, CASE..., CASE...,)
	# Check that you're working with the correct datatypes (WHEN 1 != WHEN "1")
	# Use '' instead of "" in the conditions - "City" returns the column's (City) value, 'City' returns the word 'City'

	urbanization = q("""
		SELECT
			CASE substr(locale_code,2,1)
				WHEN '1' THEN 'Large'
				WHEN '2' THEN 'Midsize'
				WHEN '3' THEN 'Small'
			END,
			CASE substr(locale_code,1,1)
				WHEN '1' THEN 'City'
				WHEN '2' THEN 'Suburb'
				WHEN '3' THEN 'Town'
				WHEN '4' THEN 'Rural'
			END
		FROM public_hs_data
	""")


	# What is the minimum, maximum, and average median_household_income of the nation? for each state?
	stats = q("""
		WITH temp (zip, state, mhi) AS (
			SELECT zip_code, state_code,
				CASE median_household_income
					WHEN 'NULL' THEN NULL
					ELSE CAST(median_household_income AS INT)
				END
			FROM census_data)
		SELECT state, min(mhi), max(mhi), round(avg(mhi),2), sum(mhi)
		FROM temp
		GROUP BY state
	""")
	# print(stats)

	# Joint analysis: Join the tables together for even more analysis.
	# Do characteristics of the zip-code area, such as median household income, influence students’ performance in high school?
	# Hint: One option would be to use the CASE statement to divide the median_household_income
	# into income ranges (e.g., <$50k, $50k-$100k, $100k+) and find the average exam scores for each.

	# in the WITH statement, CASE-> CAST val as REAL + add type (hs, uni, etc.) to new column

	x = q("""

		WITH census (income, perc_pop, edu_lvl) AS (
		-- WITH census (hs, col1yr, col1yrplus, assoc, bach, mast, prof, doct) AS (
			SELECT
			CASE
				WHEN median_household_income < 50000 THEN 'LOW'
				WHEN median_household_income > 50000 THEN 'MEDIUM'
				WHEN median_household_income < 10000 THEN 'HIGH'
			END,
			CASE
				WHEN pct_edu_hs THEN CAST(pct_edu_hs AS REAL)
				WHEN pct_edu_somecollege_under1yr THEN CAST(pct_edu_somecollege_under1yr AS REAL)
				WHEN pct_edu_somecollege_1plusyrs THEN CAST(pct_edu_somecollege_1plusyrs AS REAL)
				WHEN pct_edu_attain_assoc THEN CAST(pct_edu_attain_assoc AS REAL)
				WHEN pct_edu_attain_bach THEN CAST(pct_edu_attain_bach AS REAL)
				WHEN pct_edu_attain_master THEN CAST(pct_edu_attain_master AS REAL)
				WHEN pct_edu_attain_prof THEN CAST(pct_edu_attain_prof AS REAL)
				WHEN pct_edu_attain_doct THEN CAST(pct_edu_attain_doct AS REAL)
			END,
			CASE
				WHEN pct_edu_hs THEN 'hs'
				WHEN pct_edu_somecollege_under1yr THEN 'somecollege_under1yr'
				WHEN pct_edu_somecollege_1plusyrs THEN 'somecollege_1plusyrs'
				WHEN pct_edu_attain_assoc THEN 'attain_assoc'
				WHEN pct_edu_attain_bach THEN 'attain_bach'
				WHEN pct_edu_attain_master THEN 'attain_master'
				WHEN pct_edu_attain_prof THEN 'attain_prof'
				WHEN pct_edu_attain_doct THEN 'attain_doct'
			END
			FROM census_data)

			SELECT income
			FROM census

		-- WITH census (zip_code, state_code, mhi) AS (
		-- 	SELECT zip_code, state_code,
		-- 		CASE median_household_income
		-- 			WHEN 'NULL' THEN NULL
		-- 			ELSE CAST(median_household_income AS INT)
		-- 		END
		-- 	FROM census_data)

		-- 	SELECT
		-- 		CASE
		-- 			WHEN census.mhi < 50000 THEN 'LOW'
		-- 			WHEN census.mhi > 50000 THEN 'MEDIUM'
		-- 			WHEN census.mhi < 10000 THEN 'HIGH'
		-- 		END AS income

		-- 	FROM census
		-- 		INNER JOIN public_hs_data public
		-- 		ON census.state_code = public.state_code
		-- 		AND census.zip_code = public.zip_code

		-- 	GROUP BY income

	""")

	print(x)

	# q5 = q("""
	# 	WITH census (zip, state) as (
	# 		SELECT zip_code, state_code
	# 		FROM census_data
	# 	)
	# 	SELECT public.zip_code
	# 	FROM public_hs_data public
	# 		LEFT JOIN census
	# 		ON public.zip_code = census.zip
	# 	WHERE census.zip IS NULL
	# 	GROUP BY public.zip_code
	# """)
	# q6 = q("""
	# 	WITH census (zip, state) as (
	# 		SELECT zip_code, state_code
	# 		FROM census_data
	# 	)
	# 	SELECT public.state_code
	# 	FROM public_hs_data public
	# 		LEFT JOIN census
	# 		ON public.state_code = census.state
	# 	WHERE census.state IS NULL
	# 	GROUP BY public.state_code
	# """)


def intermediate():
	pass


def advanced():
	pass


basic()
# intermediate()
# advanced()
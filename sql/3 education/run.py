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

	income_vs_level_education = q("""

		WITH census (income, perc_pop, edu_lvl) AS (
			SELECT
			CASE
				WHEN CAST(median_household_income AS INT) > 50000 THEN 'LOW'
				WHEN CAST(median_household_income AS INT) BETWEEN 50000 AND 100000 THEN 'MEDIUM'
				WHEN CAST(median_household_income AS INT) < 100000 THEN 'HIGH'
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
				WHEN pct_edu_hs THEN 0
				WHEN pct_edu_somecollege_under1yr THEN 1
				WHEN pct_edu_somecollege_1plusyrs THEN 2
				WHEN pct_edu_attain_assoc THEN 3
				WHEN pct_edu_attain_bach THEN 4
				WHEN pct_edu_attain_master THEN 5
				WHEN pct_edu_attain_prof THEN 6
				WHEN pct_edu_attain_doct THEN 7
			END
			FROM census_data)

			SELECT income, avg(edu_lvl), min(edu_lvl), max(edu_lvl)
			FROM census
			GROUP BY income
	""")


def intermediate():
	# On average, do students perform better on the math or reading exam? Find the number of states where students do better on the math exam, and vice versa.
	# Hint: We can use the WITH clause to create a temporary table of average exam scores for each state, with an additional column for whether the average
	# for math or reading is higher. (Note: Some states may not have standardized assessments, so be sure to also include an option for No Exam Data)
	# Then, in your final SELECT statement, find the number of states fitting each condition.

	math_reading_results = q("""
		SELECT avg(pct_proficient_math), avg(pct_proficient_reading)
		FROM public_hs_data
	""")

	math_reading_results_by_state = q("""

		WITH preferred (state, avg_math, avg_read, higher) AS (
			SELECT state_code, avg(pct_proficient_math), avg(pct_proficient_reading),
			CASE
				WHEN avg(pct_proficient_math) > avg(pct_proficient_reading) THEN 'math'
				WHEN avg(pct_proficient_reading) > avg(pct_proficient_math) THEN 'reading'
				ELSE 'no data'
			END
			FROM public_hs_data
			GROUP BY state_code
		)

		SELECT COUNT(higher)
		FROM preferred
		GROUP BY higher

	""")

def advanced():
	# What is the average proficiency on state assessment exams for each zip code, and how do they compare to other zip codes in the same state?
	# Note: Exam standards may vary by state, so limit comparison within states. Some states may not have exams. We can use the WITH clause to
	# create a temporary table of exam score statistic for each state (e.g., min/max/avg) - then join it to each zip-code level data to compare.

	


# basic()
# intermediate()
advanced()
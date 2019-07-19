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
		SELECT state, min(mhi), max(mhi), avg(mhi), sum(mhi)
		FROM temp
		GROUP BY state
	""")
	print(stats)


def intermediate():
	pass


def advanced():
	pass


basic()
# intermediate()
# advanced()
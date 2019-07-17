import sqlite3
import os
import csv
import json
import math
from datetime import datetime as dt

# https://discuss.codecademy.com/t/data-science-independent-project-1-watching-the-stock-market/419943/1

stock_names = ['Bank of America', 'LivePerson, Inc.', 'Workday Inc']

connection = sqlite3.connect('stocks.db')
crsr = connection.cursor()


def create_table():

	create_table_stmt = """
	CREATE TABLE stocks (
		`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		`symbol` TEXT NOT NULL,
		`name` TEXT NOT NULL,
		`date` TEXT NOT NULL,
		`price` REAL NOT NULL )
	"""

	try:
		crsr.execute(create_table_stmt)
	except sqlite3.OperationalError:
		pass



def insert_data():

	files = [file for file in os.listdir('data')]

	for i in range(3):

		file = files[i]
		name = stock_names[i]
		symbol = file.split('.')[0]

		f = os.path.join('data', file)
		with open(f, newline='') as csvfile:
			reader = csv.DictReader(csvfile)

			for row in reader:
				date = '{} {}'.format(row['Date'], dt.now().strftime("%H-%M-%S-%f"))
				price = row['Close']

				insert_stmt = "INSERT INTO stocks (symbol, name, date, price) VALUES ('{}', '{}', '{}', '{}')".format(
					symbol, name, date, price)

				crsr.execute(insert_stmt)

	connection.commit()


def basic_queries():

	for stock in stock_names:


		# What are the distinct stocks in the table?
		q1 = "SELECT name, count(*) FROM stocks WHERE name = '{0}' GROUP BY '{0}'".format(stock)


		# Query all data for a single stock. Do you notice any overall trends?
		q2 = "SELECT * FROM stocks WHERE name = '{}'".format(stock)


	# Which rows have a price above 100? between 40 to 50, etc?
	q3 = "SELECT * FROM stocks WHERE price > 100"
	q4 = "SELECT * FROM stocks WHERE price >= 15 AND price <= 30"


	# Sort the table by price. What are the minimum and maximum prices?
	q5 = "SELECT * FROM stocks ORDER BY price DESC"


def intermediate_queries():

	def day_of_week(s):
		return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'][dt.strptime(s, '%Y-%m-%d %H-%M-%S-%f').weekday()]


	# Explore using aggregate functions to look at key statistics about the data (e.g., min, max, average).
	qs = ("SELECT min(price) FROM stocks",
		"SELECT max(price) FROM stocks",
		"SELECT avg(price) FROM stocks",)


	# Group the data by stock and repeat. How do the stocks compare to each other?
	for stock in stock_names:

		qs = ("SELECT min(price) FROM stocks WHERE name = '{}'".format(stock),
			"SELECT max(price) FROM stocks WHERE name = '{}'".format(stock),
			"SELECT avg(price) FROM stocks WHERE name = '{}'".format(stock),)


	# Group the data by day. Does day of week impact prices?
	qs = [result for result in crsr.execute("SELECT name, date, price FROM stocks")]

	stocks_by_week = {
		stock: {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [],
		} for stock in stock_names}

	for result in qs:
		stocks_by_week[ result[0] ][ day_of_week(result[1]) ].append( result[2] )

	key_figs = {}

	for stock in stocks_by_week:
		key_figs[stock] = {}
		for day in stocks_by_week[stock]:
			key_figs[stock][day] = {}
			vals = stocks_by_week[stock][day]

			for stat in (
				('min', min),
				('avg', lambda l: (sum(l)/len(l))),
				('max', max),):

				key_figs[stock][day][stat[0]] = stat[1](vals)

	# print(json.dumps(key_figs, sort_keys=True, indent=4))


	# Which of the rows have a price greater than the average of all prices in the dataset?
	qs = crsr.execute("SELECT * FROM stocks WHERE price > (SELECT avg(price) FROM stocks)")


def advanced_queries():

	# In addition to the built-in aggregate functions, explore ways to calculate
	# other key statistics about the data, such as the median or variance.

	# MEDIAN
	qs1 = crsr.execute("SELECT * FROM stocks ORDER BY price LIMIT 1 OFFSET (SELECT COUNT(*) FROM stocks)/2")

	# VARIANCE
	def square(value):
		return value**2

	def stddev(values):
		return math.sqrt( sum(values)/len(values) )

	connection.create_function("square", 1, square)

	# Assign variable for average price so that it's not re-calculated for each row
	# SQLite doesn't have this capability so store value in temporary table
	crsr.execute("CREATE TEMP TABLE _Variables(RealValue REAL)")
	crsr.execute("INSERT INTO _Variables (RealValue) SELECT avg(price) FROM stocks")

	qs2 = crsr.execute("SELECT square( price-(SELECT RealValue FROM _Variables LIMIT 1) ) FROM stocks")
	variance = stddev([i[0] for i in qs2])
	crsr.execute("DROP TABLE _Variables")

	# Let’s refactor the data into 2 tables - stock_info to store general info about the stock itself
	# (ie. symbol, name)and stock_prices to store the collected data on price (ie. symbol, datetime, price).

	def create_new_tables():
		crsr.execute("CREATE TABLE stock_info AS SELECT DISTINCT symbol, name FROM stocks")
		crsr.execute("CREATE TABLE stock_prices AS SELECT symbol, date, price FROM stocks")
		connection.commit()

	# create_new_tables()


	# Don’t forget to also drop certain columns from the original table and rename it.

	def alter_old_table():
		crsr.execute("ALTER TABLE stocks RENAME TO temp_table")
		crsr.execute("CREATE TABLE old_stocks_table AS SELECT symbol, date, price FROM temp_table")
		crsr.execute("DROP TABLE temp_table")
		connection.commit()

	# alter_old_table()


	# Now, we do not need to repeat both symbol and name for each row of price data. Instead,
	# join the 2 tables in order to view more information on the stock with each row of price

	# qs3 = crsr.execute("SELECT i.symbol, i.name, p.date, p.price FROM stock_info AS i JOIN stock_prices AS p")


	# Add more variables to the stock_info table and update the data (e.g., sector, industry, etc).

	def add_columns():
		crsr.execute("ALTER TABLE stock_info ADD sector TEXT")
		crsr.execute("ALTER TABLE stock_info ADD industry TEXT")
		connection.commit()

	# add_columns()

	def insert_extras():
		crsr.execute("UPDATE stock_info SET sector='Financial Services', industry='Banks - Global' WHERE symbol = 'BAC' ")
		crsr.execute("UPDATE stock_info SET sector='Technology', industry='Software - Infrastructure' WHERE symbol = 'LPSN' ")
		crsr.execute("UPDATE stock_info SET sector='Technology', industry='Software - Application' WHERE symbol = 'WDAY' ")
		connection.commit()

	# insert_extras()


# create_table()
# insert_data()
# basic_queries()
# intermediate_queries()
advanced_queries()
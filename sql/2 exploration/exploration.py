import sqlite3
import os

# https://discuss.codecademy.com/t/data-science-independent-project-2-explore-a-sample-database/419945

connection = sqlite3.connect('chinook.db')
crsr = connection.cursor()

tables = [i for i in crsr.execute("SELECT name FROM sqlite_master WHERE type='table'")]
# print(tables)
tables_and_info = [i for i in crsr.execute("SELECT * FROM sqlite_master")]

def basic_requirements():

	# Which tracks appeared in the most playlists? how many playlist did they appear in?
	crsr.execute("CREATE TEMP TABLE _Variables(RealValue REAL)")

	max_count_amongst_playlists = crsr.execute("""
		INSERT INTO _Variables (RealValue)
		SELECT count(*)
		FROM playlist_track
		GROUP BY TrackID
		ORDER BY count(*) DESC
		LIMIT 1
	""")

	most_common_playlist_tracks_and_pl_count = [i for i in crsr.execute("""
		SELECT count(*), t.Name

		FROM playlist_track p
		JOIN tracks t
			ON p.TrackId = t.TrackId

		GROUP BY p.TrackId
			HAVING count(*) = (SELECT * FROM _Variables)

		ORDER BY count(*) DESC, t.TrackID ASC
	""")]


	# Which track generated the most revenue? which album? which genre?

	most_lucrative_tracks = [i for i in crsr.execute("""
		SELECT track.name, sum(invoice.UnitPrice), album.Title, genre.Name

		FROM invoice_items invoice
		LEFT JOIN tracks track
			ON invoice.TrackID = track.TrackID
		LEFT JOIN albums album
			ON track.AlbumID = album.AlbumID
		LEFT JOIN genres genre
			ON track.GenreID = genre.GenreID

		GROUP BY invoice.TrackID
			HAVING sum(invoice.UnitPrice) = ( SELECT sum(UnitPrice) FROM invoice_items
										GROUP BY TrackID
										ORDER BY sum(UnitPrice)
										DESC LIMIT 1 )

		ORDER BY sum(invoice.UnitPrice) DESC, track.TrackID ASC
	""")]

	most_lucrative_albums = [i for i in crsr.execute("""
		SELECT album.Title, round(sum(invoice.UnitPrice), 2)

		FROM invoice_items invoice
		LEFT JOIN tracks track
			ON invoice.TrackID = track.TrackID
		LEFT JOIN albums album
			ON track.AlbumId = album.AlbumId

		GROUP BY album.AlbumId

		ORDER BY sum(invoice.UnitPrice) DESC
	""")]

	most_lucrative_genres = [i for i in crsr.execute("""
		SELECT genre.Name, round(sum(invoice.UnitPrice), 2)

		FROM invoice_items invoice
		LEFT JOIN tracks track
			ON invoice.TrackID = track.TrackID
		LEFT JOIN genres genre
			ON track.GenreID = genre.GenreID

		GROUP BY genre.GenreID

		ORDER BY sum(invoice.UnitPrice) DESC
	""")]

	# Which countries have the highest sales revenue? What percent of total revenue does each country make up?
	sales_by_country = [i for i in crsr.execute("""
		SELECT BillingCountry, round(sum(Total), 2), round((sum(Total)/(SELECT sum(Total) FROM invoices)*100), 2)
		FROM invoices
		GROUP BY BillingCountry
		ORDER BY sum(Total) DESC
	""")]

	# How many customers did each employee support, what is the average revenue for each sale, and what is their total sale?
	employee_sales_figures = [i for i in crsr.execute("""
		SELECT employee.Email, count(customer.CustomerID), round((sum(invoice.Total)/count(customer.CustomerID)),2), round(sum(invoice.Total),2)
		FROM invoices invoice
		LEFT JOIN customers customer
			ON invoice.CustomerId = customer.CustomerId
		LEFT JOIN employees employee
			ON customer.SupportRepId = employee.employeeId

		GROUP BY employee.employeeId
	""")]



def intermediate_challenges():
	# Do longer or shorter length albums tend to generate more revenue?
	# Hint: We can use the WITH clause to create a temporary table that determines the number of tracks in each album,
	# then group by the length of the album to compare the average revenue generated for each.
	# https://blog.expensify.com/2015/09/25/the-simplest-sqlite-common-table-expression-tutorial/ < good explanation/examples of WITH clause
	album_lengths_vs_revenue = [i for i in crsr.execute("""
		SELECT * FROM (SELECT 1)
		-- SELECT count(track.TrackId), sum(invoice.UnitPrice)
		-- FROM invoice_items invoice
		-- JOIN tracks track
		-- 	ON invoice.TrackId = track.TrackId
		-- JOIN albums album
		-- 	ON track.TrackId = album.AlbumId
		-- GROUP BY count(track.TrackId)
	""")]
	print(album_lengths_vs_revenue)

	# Is the number of times a track appear in any playlist a good indicator of sales?
	# Hint: We can use the WITH clause to create a temporary table that determines the number of times each track appears
	# in a playlist, then group by the number of times to compare the average revenue generated for each.

def advanced_challenges():
	pass
	# How much revenue is generated each year, and what is its percent change 3 from the previous year?
	# Hint: The InvoiceDate field is formatted as ‘yyyy-mm-dd hh:mm:ss’. Try taking a look at using the strftime() function
	# to help extract just the year. Then, we can use a subquery in the SELECT statement to query the total revenue from the
	# previous year. Remember that strftime() returns the date as a string, so we would need to CAST it to an integer type
	# for this part. Finally, since we cannot refer to a column alias in the SELECT statement, it may be useful to use the
	# WITH clause to query the previous year total in a temporary table, and then calculate the percent change in the final
	# SELECT statement.


# basic_requirements()
intermediate_challenges()

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

	# print(most_common_playlist_tracks_and_pl_count)

	# Which track generated the most revenue? which album? which genre?

	print([i for i in crsr.execute("""
		SELECT track.name, sum(invoice.UnitPrice), album.Title, genre.Name
		FROM invoice_items invoice

		JOIN tracks track
			ON invoice.TrackID = track.TrackID
		JOIN albums album
			ON track.AlbumID = album.AlbumID
		JOIN genres genre
			ON track.GenreID = genre.GenreID

		GROUP BY invoice.TrackID
			HAVING sum(invoice.UnitPrice) = ( SELECT sum(UnitPrice) FROM invoice_items
										GROUP BY TrackID
										ORDER BY sum(UnitPrice)
										DESC LIMIT 1 )

		ORDER BY sum(invoice.UnitPrice) DESC, track.TrackID ASC
	""")])

	# Which countries have the highest sales revenue? What percent of total revenue does each country make up?

	# How many customers did each employee support, what is the average revenue for each sale, and what is their total sale?

def additional_challenges():
	pass

	def intermediate_challenges():
		pass
		# Do longer or shorter length albums tend to generate more revenue?
		# Hint: We can use the WITH clause to create a temporary table that determines the number of tracks in each album,
		# then group by the length of the album to compare the average revenue generated for each.

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

basic_requirements()
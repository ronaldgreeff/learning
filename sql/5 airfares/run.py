import sqlite3
import os
from datetime import datetime as dt

# https://discuss.codecademy.com/t/data-science-independent-project-5-analyze-airfare-data/419949

connection = sqlite3.connect('db.db')
crsr = connection.cursor()


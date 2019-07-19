import sqlite3
import os
from datetime import datetime as dt

# https://discuss.codecademy.com/t/data-science-independent-project-4-home-value-trends/419948

connection = sqlite3.connect('db.db')
crsr = connection.cursor()

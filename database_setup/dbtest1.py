import sqlite3
import pandas as pd

con = sqlite3.connect('database.db')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
cursor = con.cursor()
cursor.execute("SELECT * FROM lacounty")
print(cursor.fetchall())
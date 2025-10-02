import sqlite3
import pandas as pd
import sqlalchemy
con = sqlite3.connect('database.db')
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
cursor = con.cursor()
cursor.execute("SELECT * FROM lacounty")
print(cursor.fetchall())

dbEngine=sqlalchemy.create_engine('sqlite:////Users/dmj/Jupyter/CGU/IST303/TeamKanto_GroupProject/ist-303-team-kanto-project/database_setup/database.db')

df = pd.read_sql('select * from lacounty', dbEngine)

print(df)
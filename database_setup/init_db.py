import sqlite3
import pandas as pd
import os.path
import sqlalchemy

#Hard-Coded prior to writing `csv_to_db()` function
"""
connection = sqlite3.connect('database.db')

df = pd.read_csv('LACOUNTY.csv')
with open('schema.sql') as f:
    connection.executescript(f.read())


for i in range(len(df)):

    cur = connection.cursor()
    cur.execute("INSERT INTO lacounty (idx, fac_id, fac_name, address, city, state, zip_code, county, tel_num, hosp_type, hosp_owner, emergency, birth_friendly, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                tuple(df.iloc[i])
                )

connection.commit()
connection.close()
"""

#`csv_to_db()` still requires specific schema, but writes csv to db
def csv_to_db(csv_file, db_name, schema):
    """Takes csv file and appends each """

    #Check if database already in file directory
    if os.path.isfile(db_name):
        return "Database Already Exists"
    
    #If not, create databse, write csv rows to it
    else:

        #Open  connection to empty database file
        connection = sqlite3.connect(db_name)

        #Read in csv through pandas
        df = pd.read_csv(csv_file, index_col=0)

        #Convert to string to avoid int(64) to BLOB conversion; this will need refactoring later
        for column in df:
            df[column] = df[column].apply(str)
        with open(schema) as f:
            connection.executescript(f.read())


        #Generalized column/values inputs to be placed in SQL query template
        columns = ', '.join(df.columns)
        values = ', '.join(['?']*len(df.columns))

        for i in range(len(df)):

            cur = connection.cursor()
            #print(tuple(df.iloc[i]))
            #Create a SQL query based on template plus columns, values, and row
            cur.execute(f"INSERT INTO lacounty ({columns}) VALUES ({values})",
                        tuple(df.iloc[i])
                        )

        #Commit changes to database table
        connection.commit()
        #Close the connection
        connection.close()
        #Confirm process is finished
        return "Database Initialized"



def db_check(csv_file, db_name, table_name):
    """
    Determines whether contents of csv file match contents of 
    newly-created database file.
    """
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM lacounty")

    print('Queries Succeeded')

    #Create database connection with SQLAlchemy
    dbEngine=sqlalchemy.create_engine('sqlite:///'+db_name)

    #Open old DataFrame from CSV file
    df = pd.read_csv(csv_file, index_col=0)
    #If run as standalone file, init_db will print out table data types
    print(df.info())

    #Open new DataFrame from newly-created SQL database
    df2 = pd.read_sql(f'select * from {table_name}', dbEngine)
    #If run as standalone file, init_db will print out table data types
    print(df2.info())

    #Check if columns are the same *when cast as string objects*
    for column in df2.columns:
        df2[column] = df2[column].apply(str)
    for column in df.columns:
        df[column] = df[column].apply(str)

    #for column in df.columns:
    #    print(df[column].equals(df2[column]))

    #Confirm that the data tables are the same:
    return df.equals(df2)
    

if __name__ == '__main__':

    csv_to_db('LACOUNTY.csv', 'database.db', 'schema.sql')

    print(db_check('LACOUNTY.csv', 'database.db', 'lacounty'))
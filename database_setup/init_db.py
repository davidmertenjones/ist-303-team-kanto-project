import sqlite3
import pandas as pd
import os.path
import sqlalchemy

"""connection = sqlite3.connect('database.db')

df = pd.read_csv('LACOUNTY.csv')
with open('schema.sql') as f:
    connection.executescript(f.read())


for i in range(len(df)):

    cur = connection.cursor()
    cur.execute("INSERT INTO lacounty (idx, fac_id, fac_name, address, city, state, zip_code, county, tel_num, hosp_type, hosp_owner, emergency, birth_friendly, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                tuple(df.iloc[i])
                )

connection.commit()
connection.close()"""


def csv_to_db(csv_file, db_name, schema):
    """Takes csv file and appends each """

    if os.path.isfile(db_name):
        return "Database Already Exists"
    else:

        connection = sqlite3.connect(db_name)

        df = pd.read_csv(csv_file, index_col=0)
        for column in df:
            df[column] = df[column].apply(str)
        with open(schema) as f:
            connection.executescript(f.read())

        columns = ', '.join(df.columns)
        values = ', '.join(['?']*len(df.columns))

        for i in range(len(df)):

            cur = connection.cursor()
            #print(tuple(df.iloc[i]))
            cur.execute(f"INSERT INTO lacounty ({columns}) VALUES ({values})",
                        tuple(df.iloc[i])
                        )

        connection.commit()
        connection.close()
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

    dbEngine=sqlalchemy.create_engine('sqlite:///'+db_name)

    #Old DataFrame from CSV file
    df = pd.read_csv(csv_file, index_col=0)

    #DataFrame from newly-created SQL database
    df2 = pd.read_sql(f'select * from {table_name}', dbEngine)

    for column in df.columns:
        df[column] = df[column].apply(str)

    return df.equals(df2)



if __name__ == '__main__':
    csv_to_db('LACOUNTY.csv', 'database.db', 'schema.sql')
    print(db_check('LACOUNTY.csv', 'database.db', 'lacounty'))
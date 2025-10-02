import sqlite3
import pandas as pd


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
        print(tuple(df.iloc[i]))
        cur.execute(f"INSERT INTO lacounty ({columns}) VALUES ({values})",
                    tuple(df.iloc[i])
                    )

    connection.commit()
    connection.close()


if __name__ == '__main__':
    csv_to_db('LACOUNTY.csv', 'database.db', 'schema.sql')
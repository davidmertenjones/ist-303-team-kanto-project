from init_db import *
import pytest

@pytest.mark.parametrize(
		"csv_file, db_name, schema, message",[
			('LACOUNTY.csv', 'database.db', "schema.sql", 'Database Initialized'),
	        ('LACOUNTY.csv', 'database.db', "schema.sql", 'Database Already Exists') 
	    ]
	)
def test_csv_to_db(csv_file, db_name, schema, message):
	assert csv_to_db(csv_file, db_name, schema) == message
	

@pytest.mark.parametrize(
		"csv_file, db_name, table_name, message",[
			('LACOUNTY.csv', 'database.db', "lacounty", True)
			]
	)
def test_db_check(csv_file, db_name, table_name, message):
	assert db_check(csv_file, db_name, table_name) == message

	
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import csv
#from app import User
app = Flask(__name__)

def init_db():
    with app.app_context():
        db.create_all()
        load_data()
        print('data loaded')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Hospital(db.Model):
        
    fac_id = db.Column(db.String(100), primary_key=True)
    fac_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(500), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    county = db.Column(db.String(100), nullable=False)
    tel_num = db.Column(db.String(100), nullable=False)
    hosp_type = db.Column(db.String(100), nullable=False)
    hosp_owner = db.Column(db.String(100), nullable=False)
    emergency = db.Column(db.String(100), nullable=False)
    maternity = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

def load_data():

    hospital_data = []

    with open('LACOUNTY.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hospital_data.append(row)

    for h in hospital_data:
        hospital = Hospital(
            fac_id=h['fac_id'],
            fac_name=h['fac_name'], 
            address=h['address'], 
            city=h['city'], 
            state=h['state'], 
            zip_code=h['zip_code'], 
            county=h['county'], 
            tel_num=h['tel_num'], 
            hosp_type=h['hosp_type'], 
            hosp_owner=h['hosp_owner'], 
            emergency=h['emergency'], 
            maternity=h['maternity'],
            rating=h['rating']
        )

        db.session.add(hospital)

    db.session.commit() 

init_db()

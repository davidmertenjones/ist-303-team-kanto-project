from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import UserMixin
from flask_security import Security, RoleMixin, UserMixin, hash_password, SQLAlchemySessionUserDatastore
import csv
from flask_bcrypt import Bcrypt
import uuid
#from app import User
app = Flask(__name__)

def init_db():
    with app.app_context():
        db.create_all()
        create_roles()
        load_hospital_data()
        load_user_data()
        print('data loaded')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

#from app import Role, db, app

def create_roles():
    with app.app_context():
        admin = Role(id=1, name='Admin')
        provider = Role(id=2, name='Provider')
        user = Role(id=3, name='User')
        
        db.session.add(admin)
        db.session.add(provider)
        db.session.add(user)

        db.session.commit()
        print("Roles created successfully!")


user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

#User database model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)
    roles = db.relationship('Role', secondary=user_roles, backref='roled')

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

#Hospital database model (pre-loads from LACOUNTY.csv)
class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.String(100), primary_key=True)
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
    rating = db.Column(db.String(2), nullable=False)
    urgent_care = db.Column(db.Integer, nullable=False)
    psychiatric = db.Column(db.Integer, nullable=False)
    childrens = db.Column(db.Integer, nullable=False)
    veterans = db.Column(db.Integer, nullable=False)

def load_hospital_data():

    hospital_data = []

    with open('LACOUNTY.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hospital_data.append(row)

    for h in hospital_data:
        hospital = Hospital(
            id=h['fac_id'],
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
            rating=h['rating'],
            urgent_care=h['urgent_care'],
            psychiatric=h['psychiatric'],
            childrens=h['childrens'],
            veterans=h['veterans']
        )

        db.session.add(hospital)

    db.session.commit() 

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)




def load_user_data():

    roles_dict = {
        "Admin":Role.query.filter(Role.id == 1).limit(1).all(),
        "Provider":Role.query.filter(Role.id == 2).limit(1).all(),
        "User":Role.query.filter(Role.id == 3).limit(1).all()
    }
    print(roles_dict)

    user_data = []

    with open('user_accounts.csv', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_data.append(row)

    for u in user_data:
        id = int(u['id'])
        hashed_password = bcrypt.generate_password_hash(u['password'])

        user = User(
            id = id,
            username = u['username'],
            email = u['email'],
            password = hashed_password,
            active = True,
            fs_uniquifier = uuid.uuid4().hex,
            roles = Role.query.filter(Role.id == u['role']).limit(1).all()
        )
    
        db.session.add(user)

    db.session.commit()

init_db()


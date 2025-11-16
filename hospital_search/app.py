

from flask import Flask, render_template, url_for, redirect, flash, request

from flask_sqlalchemy import SQLAlchemy
#Removed UserMixin from flask_login imports
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_security import Security, SQLAlchemySessionUserDatastore, roles_accepted, UserMixin, RoleMixin
import uuid
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#### PASSWORD ENCRYPTION ####

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'thisisasecretkey'
if 'SECURITY_PASSWORD_SALT' not in app.config:
    app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

db = SQLAlchemy()

db.init_app(app)

#### LOGIN MANAGER ####

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#### ASSOCIATION TABLE ####

#### DATABASES ####

######## RUN "init_db.py" FIRST TO SET UP DATABASES

roles_users = db.Table('roles_users',
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
    roles = db.relationship('Role', secondary=roles_users, backref='roled')

#Roles database model

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


#### FORMS ####

class SignupForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    email = EmailField(validators=[
                           InputRequired(), Email()], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Signup')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


#### ROUTES ####
#home - main "search by location" page
#search - loads search results dynamically within home
#signup - create new user, store in users table
#login - query users table for existing user, match password
#dashboard - [this page intentionally left blank]
#logout - logs user out (won't be able to access dashboard without logging back in), returns to home

#home - main "search by location" page
@app.route("/")
def home():
    return render_template("home.html")

#search_by_name - search page with input
@app.route("/search-by-name")
def search_by_name():
    return render_template("search_by_name.html")

#search_by_service - service selection page
@app.route("/search-by-service")
def search_by_service():
    service = request.args.get("service")
    print(service)
    return render_template("search_by_service.html")

#### These five functions should be refactored to one function ####
# service_urgent
# service_maternity
# service_childrens
# service_veterans
# service_psychiatric

@app.route("/service_urgent")
def service_urgent():
    results = Hospital.query.filter(Hospital.urgent_care.icontains(1)).limit(100).all()
    return render_template("search_results.html", results=results)

@app.route("/service_maternity")
def service_maternity():
    results = Hospital.query.filter(Hospital.maternity.icontains(1)).limit(100).all()
    return render_template("search_results.html", results=results)

@app.route("/service_childrens")
def service_pediatric():
    results = Hospital.query.filter(Hospital.childrens.icontains(1)).limit(100).all()
    return render_template("search_results.html", results=results)

@app.route("/service_veterans")
def service_veterans():
    results = Hospital.query.filter(Hospital.veterans.icontains(1)).limit(100).all()
    return render_template("search_results.html", results=results)

@app.route("/service_psychiatric")
def service_psychiatric():
    results = Hospital.query.filter(Hospital.urgent_care.icontains(1)).limit(100).all()
    return render_template("search_results.html", results=results)






#search_by_location - alias to search_by_name
@app.route("/search-by-location")
def search_by_location():
    return render_template("search_by_name.html")

#search - loads search results dynamically within home
@app.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = Hospital.query.filter(Hospital.city.icontains(q) | Hospital.zip_code.icontains(q) | Hospital.fac_name.icontains(q)).limit(10).all()
    else:
        results = []

    return render_template("search_results.html", results=results)

#signup - create new user, store in users table
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = form.password.data
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

#login - query users table for existing user, match password
@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                error = 'Incorrect Password'  
        else:
            error = 'Invalid User'
    return render_template('login_.html', form=form, error=error)

#dashboard - not accessible unless logged-in [this page intentionally left blank]
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

#logout - logs user out (won't be able to access dashboard without logging back in), returns to home
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
@roles_accepted('admin')
def admin_panel():
    return render_template('admin_panel.html')


from flask import Flask, render_template, url_for, redirect, flash, request

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
app = Flask(__name__)

#### PASSWORD ENCRYPTION ####

bcrypt = Bcrypt(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'thisisasecretkey'

db.init_app(app)

#### LOGIN MANAGER ####

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#### DATABASES ####

######## RUN "init_db.py" FIRST TO SET UP DATABASES

#User database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

#Hospital database model (pre-loads from LACOUNTY.csv)
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
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

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
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

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
@ app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
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
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                error = 'Incorrect Password'  
        else:
            error = 'Invalid User'
    return render_template('login.html', form=form, error=error)

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




from flask import Flask, render_template, url_for, redirect, flash, request

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, Email, NumberRange
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
def load_user(id):
    return User.query.get(int(id))

#### DATABASES ####

######## RUN "init_db.py" FIRST TO SET UP DATABASES

#User database model
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')
    
    @property
    def is_admin(self):
        return self.role == 'admin'

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

#Review database model - stores user reviews for hospitals (supports anonymous)
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for anonymous
    user_name = db.Column(db.String(50), nullable=True)  # For anonymous reviewers
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    is_verified = db.Column(db.Integer, default=0)  # 1 if from logged-in user
    
    @property
    def reviewer_name(self):
        """Get reviewer name (logged-in username or anonymous name)"""
        if self.user_id:
            user = User.query.get(self.user_id)
            return user.username if user else "Unknown"
        return self.user_name or "Anonymous"
    
    @property
    def is_anonymous(self):
        """Check if review is from anonymous user"""
        return self.user_id is None

#Service database model - stores services offered by hospitals (managed by admins)
class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.String(100), db.ForeignKey('hospital.id'), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Integer, default=1)  # 1 = active, 0 = inactive
    created_at = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.String(50), nullable=False)

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

class ReviewForm(FlaskForm):
    hospital_name = StringField(validators=[
                           InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Hospital Name"})
    
    rating = IntegerField(validators=[
                           InputRequired(), NumberRange(min=1, max=5)], render_kw={"placeholder": "Rating (1-5)"})
    
    comment = TextAreaField(validators=[
                           InputRequired(), Length(min=10, max=500)], render_kw={"placeholder": "Share your experience..."})

class PublicFeedbackForm(FlaskForm):
    hospital_name = StringField(validators=[
                           InputRequired(), Length(min=2, max=100)], render_kw={"placeholder": "Hospital Name"})
    
    your_name = StringField(validators=[
                           InputRequired(), Length(min=2, max=50)], render_kw={"placeholder": "Your Name"})
    
    rating = IntegerField(validators=[
                           InputRequired(), NumberRange(min=1, max=5)], render_kw={"placeholder": "Rating (1-5)"})
    
    comment = TextAreaField(validators=[
                           InputRequired(), Length(min=10, max=500)], render_kw={"placeholder": "Share your experience..."})
    
    submit = SubmitField('Submit Feedback')

class ServiceForm(FlaskForm):
    service_name = StringField(validators=[
                           InputRequired(), Length(min=3, max=100)], render_kw={"placeholder": "Service Name"})
    
    description = TextAreaField(validators=[
                           Length(max=500)], render_kw={"placeholder": "Description (optional)"})
    
    submit = SubmitField('Save Service')

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

@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin_panel.html')

#review - allows logged-in users to submit reviews
@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    
    if form.validate_on_submit():
        from datetime import datetime
        new_review = Review(
            hospital_name=form.hospital_name.data,
            user_id=current_user.id,
            rating=form.rating.data,
            comment=form.comment.data,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_verified=1
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Thank you for your review!', 'success')
        return redirect(url_for('review'))
    
    # Get recent reviews from this user
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).limit(5).all()
    
    return render_template('review.html', form=form, user_reviews=user_reviews)

#### PUBLIC FEEDBACK (NO LOGIN REQUIRED) ####

@app.route('/feedback', methods=['GET', 'POST'])
def public_feedback():
    """Public feedback submission - no login required"""
    form = PublicFeedbackForm()
    
    if form.validate_on_submit():
        from datetime import datetime
        new_feedback = Review(
            hospital_name=form.hospital_name.data,
            user_id=None,  # Anonymous
            user_name=form.your_name.data,
            rating=form.rating.data,
            comment=form.comment.data,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            is_verified=0  # Not verified
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('view_feedback', hospital_name=form.hospital_name.data))
    
    return render_template('public_feedback.html', form=form)

@app.route('/feedback/view/<path:hospital_name>')
def view_feedback(hospital_name):
    """View all feedback for a specific hospital"""
    reviews = Review.query.filter_by(hospital_name=hospital_name).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
    else:
        avg_rating = 0
    
    return render_template('view_feedback.html', 
                         hospital_name=hospital_name,
                         reviews=reviews,
                         avg_rating=round(avg_rating, 1),
                         total_reviews=len(reviews))

@app.route('/feedback/all')
def all_feedback():
    """View all hospitals with feedback"""
    # Get unique hospital names with review counts and averages
    from sqlalchemy import func
    hospitals = db.session.query(
        Review.hospital_name,
        func.count(Review.id).label('review_count'),
        func.avg(Review.rating).label('avg_rating')
    ).group_by(Review.hospital_name).all()
    
    return render_template('all_feedback.html', hospitals=hospitals)

#### SERVICE MANAGEMENT (ADMIN ONLY) ####

@app.route('/admin/services')
@login_required
def manage_services():
    """Admin view: manage all hospital services"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    # Get all hospitals with their services
    hospitals = Hospital.query.limit(10).all()  # Limit to first 10 for performance
    
    # Get services for each hospital
    hospital_services = {}
    for hospital in hospitals:
        hospital_services[hospital.id] = Service.query.filter_by(hospital_id=hospital.id).all()
    
    return render_template('manage_services.html', hospitals=hospitals, hospital_services=hospital_services)

@app.route('/admin/service/add/<hospital_id>', methods=['GET', 'POST'])
@login_required
def add_service(hospital_id):
    """Admin: add a new service to a hospital"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    hospital = Hospital.query.get_or_404(hospital_id)
    form = ServiceForm()
    
    if form.validate_on_submit():
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_service = Service(
            hospital_id=hospital_id,
            service_name=form.service_name.data,
            description=form.description.data,
            is_active=1,
            created_at=timestamp,
            updated_at=timestamp
        )
        db.session.add(new_service)
        db.session.commit()
        flash(f'Service "{new_service.service_name}" added successfully!', 'success')
        return redirect(url_for('manage_services'))
    
    return render_template('service_form.html', form=form, hospital=hospital, action='Add')

@app.route('/admin/service/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    """Admin: edit an existing service"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    service = Service.query.get_or_404(service_id)
    hospital = Hospital.query.get(service.hospital_id)
    form = ServiceForm()
    
    if form.validate_on_submit():
        from datetime import datetime
        service.service_name = form.service_name.data
        service.description = form.description.data
        service.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        flash(f'Service "{service.service_name}" updated successfully!', 'success')
        return redirect(url_for('manage_services'))
    
    elif request.method == 'GET':
        form.service_name.data = service.service_name
        form.description.data = service.description
    
    return render_template('service_form.html', form=form, hospital=hospital, service=service, action='Edit')

@app.route('/admin/service/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    """Admin: deactivate a service (soft delete)"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    service = Service.query.get_or_404(service_id)
    service.is_active = 0  # Soft delete
    db.session.commit()
    flash(f'Service "{service.service_name}" has been deactivated.', 'success')
    return redirect(url_for('manage_services'))

@app.route('/admin/service/activate/<int:service_id>', methods=['POST'])
@login_required
def activate_service(service_id):
    """Admin: reactivate a service"""
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    service = Service.query.get_or_404(service_id)
    service.is_active = 1  # Reactivate
    db.session.commit()
    flash(f'Service "{service.service_name}" has been activated.', 'success')
    return redirect(url_for('manage_services'))

#### RUN THE APP ####
if __name__ == '__main__':
    app.run(debug=True, port=5000)
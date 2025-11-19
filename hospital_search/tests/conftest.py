import pytest
import os
import tempfile
from app import app, db, bcrypt, User, Hospital, Role

@pytest.fixture(scope='session')
def test_client():
    # Configure test database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # add test hospital data - updated
            test_hospital = Hospital(
                id='test_hosp_001',  # CHANGED from fac_id to id
                fac_name='Test Hospital',
                address='123 Test St',
                city='Los Angeles',
                state='CA',
                zip_code=90001,
                county='Los Angeles',
                tel_num='555-1234',
                hosp_type='General',
                hosp_owner='Private',
                emergency='Yes',
                maternity='Yes',
                rating='4',
                urgent_care=1,
                psychiatric=0,
                childrens=0,
                veterans=0
            )
            db.session.add(test_hospital)
            db.session.commit()
            
        yield client
        
        with app.app_context():
            db.drop_all()

@pytest.fixture
def init_database(test_client):
    """Initialize database with test data"""
    # This runs before each test
    yield db

@pytest.fixture
def new_user():
    user = User(
        username='testuser',
        email='test@example.com',
        password=bcrypt.generate_password_hash('testpassword123').decode('utf-8')
    )
    return user

@pytest.fixture
def authenticated_client(test_client):
    """Create an authenticated client"""
    with test_client.application.app_context():
        # Create roles if they don't exist
        user_role = Role.query.filter_by(name='User').first()
        if not user_role:
            user_role = Role(name='User')
            db.session.add(user_role)
            db.session.commit()
        # Check if user already exists to avoid duplicate error
        existing_user = User.query.filter_by(username='authuser').first()
        if not existing_user:
            user = User(
                username='authuser',
                email='auth@example.com',
                password=bcrypt.generate_password_hash('authpassword123').decode('utf-8')
            )
            user.roles.append(user_role)  # Assign role
            db.session.add(user)
            db.session.commit()
        else:
            # Ensure existing user has a role
            if user_role not in existing_user.roles:
                existing_user.roles.append(user_role)
                db.session.commit()
    
    # Login
    test_client.post('/login', data={
        'username': 'authuser',
        'password': 'authpassword123'
    }, follow_redirects=True)
        
    return test_client


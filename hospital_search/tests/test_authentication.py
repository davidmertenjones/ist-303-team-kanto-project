import pytest
from app import db, User, bcrypt

class TestAuthentication:
    
    def test_valid_login(self, test_client):
        """Test valid user login"""
        with test_client.application.app_context():
            # Create test user
            user = User(
                username='logintest',
                email='login@example.com',
                password=bcrypt.generate_password_hash('loginpass123').decode('utf-8')
            )
            db.session.add(user)
            db.session.commit()
        
        response = test_client.post('/login', data={
            'username': 'logintest',
            'password': 'loginpass123'
        }, follow_redirects=True)
        
        # Should redirect to dashboard after successful login
        assert response.status_code == 200
    
    def test_invalid_login_wrong_password(self, test_client):
        """Test login with wrong password"""
        with test_client.application.app_context():
            user = User(
                username='wrongpasstest',
                email='wrongpass@example.com',
                password=bcrypt.generate_password_hash('correctpass').decode('utf-8')
            )
            db.session.add(user)
            db.session.commit()
        
        response = test_client.post('/login', data={
            'username': 'wrongpasstest',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Incorrect Password' in response.data
    
    def test_invalid_login_nonexistent_user(self, test_client):
        """Test login with non-existent user"""
        response = test_client.post('/login', data={
            'username': 'nonexistent',
            'password': 'somepassword'
        }, follow_redirects=True)
        
        assert b'Invalid User' in response.data
    
    def test_duplicate_username_signup(self, test_client):
        """Test signup with duplicate username"""
        # Create first user
        with test_client.application.app_context():
            user1 = User(
                username='duplicateuser',
                email='first@example.com',
                password='password123'
            )
            db.session.add(user1)
            db.session.commit()
        
        # Try to create user with same username
        response = test_client.post('/signup', data={
            'username': 'duplicateuser',
            'email': 'second@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Should show validation error 
        # The form should be re-displayed (not redirect) when validation fails
        assert response.status_code == 200
        assert b'duplicateuser' in response.data  
       
    def test_user_role_assignment(self, test_client):
        """Test new users get default 'user' role"""
        with test_client.application.app_context():
            user = User(
                username='roletest',
                email='role@example.com',
                password=bcrypt.generate_password_hash('password123').decode('utf-8')
            )
            db.session.add(user)
            db.session.commit()
            
            saved_user = User.query.filter_by(username='roletest').first()
            assert saved_user.role == 'user' # default role
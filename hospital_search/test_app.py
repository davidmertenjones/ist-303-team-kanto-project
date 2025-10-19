# Tests in English:
# User login tests
#!	Test valid login (correct user/pw)
#!	Test nonexistent user login (wrong user, wrong pw)
#!	Test invalid login and prompt wrong password (correct user, wrong pw)
#	Test logout
# User signup test
#	Test signup 
#!	Test duplicate signup (need to fail)
#	Test signup patient form (user, pw, email format)
#	Test signup provider form (user, pw, email format, other credential/verification fields?)
# Webpage tests
#	Test home
#	[wip]Test search w/ query; test bad spelling, does the hospital exist? does zip code return correctly, is the input form correct, or if incorrect fail appropriately
# Database model tests
#	Test hospital fields
#	Test user account fields
### acceptance criteria shapes test cases ###
# possible selenium for milestone 2
# make it run


import pytest
from app import db, User, bcrypt

class TestAuthentication:  
    
    def test_valid_login(self):
        with app.test_client() as client:
            with app.app_context():
            # create test user
                user = User(
                    username='logintest',
                    email='login@example.com',
                    password=bcrypt.generate_password_hash('pass1234').decode('utf-8')
                )
                db.session.add(user)
                db.session.commit()
        
                response = client.post('/login', data={
                    'username': 'logintest',
                    'password': 'pass1234'
                })
            # redisplay for user correction
            assert response.status_code == 200
    
    def test_invalid_login_wrong_password(self):
        with app.test_client() as client:
            with app.app_context():
                user = User(
                    username='wrongpass',
                    email='wrongpass@example.com',
                    password=bcrypt.generate_password_hash('correctpass').decode('utf-8')
                )
                db.session.add(user)
                db.session.commit()
        
            response = client.post('/login', data={
                'username': 'wrongpass',
                'password': 'wrongpw'
            }, follow_redirects=True)
        
            assert b'Incorrect Password' in response.data
    
    def test_invalid_login_nonexistent_user(self):
        with app.client() as client:
            with app.app_context():
                response = test_client.post('/login', data={
                'username': 'nonexistent',
                'password': 'anypw'
            })
        
            assert b'User does not exist' in response.data
    
    def test_duplicate_username_signup(self):
        with app.client() as client:
            with app.app_context():
                user1 = User(
                    username='duplicateuser',
                    email='og@email.com',
                    password='pass1234'
                )
                db.session.add(user1)
                db.session.commit()
        
        # try to create duplicate user
            response = client.post('/signup', data={
                'username': 'duplicateuser',
                'email': 'dupe@email.com',
                'password': 'pass1234'
            })
        
        assert response.status_code == 200
        assert b'duplicateuser' in response.data  # should show the submitted username
        
        
        
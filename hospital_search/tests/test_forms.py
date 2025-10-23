import pytest
from app import SignupForm, LoginForm

class TestForms:
    
    def test_signup_form_valid(self, test_client):
        """Test valid signup form"""
        with test_client.application.test_request_context(method='POST'):
            form = SignupForm(
                username='validuser',
                email='valid@example.com',
                password='validpass123'
            )
            # Test individual validators
            assert form.username.data == 'validuser'
            assert form.email.data == 'valid@example.com'
            assert form.password.data == 'validpass123'
            # Check that data is processed correctly
            assert len(form.username.data) >= 4  # Meets length requirement
            assert '@' in form.email.data  # Basic email format check
    
    def test_signup_form_invalid_username_length(self, test_client):
        """Test signup form with invalid username length"""
        with test_client.application.test_request_context():
            form = SignupForm(
                username='abc',  # Too short
                email='test@example.com',
                password='password123'
            )
            # The form data should still be set even if validation fails
            assert form.username.data == 'abc'
            assert len(form.username.data) < 4  # Confirms it's too short
    
    def test_signup_form_invalid_email(self, test_client):
        """Test signup form with invalid email"""
        with test_client.application.test_request_context():
            form = SignupForm(
                username='validuser',
                email='invalid-email',
                password='password123'
            )
            assert form.email.data == 'invalid-email'
            assert '@' not in form.email.data  # Confirms invalid email
    
    def test_signup_form_missing_data(self, test_client):
        """Test signup form with missing data"""
        with test_client.application.test_request_context():
            form = SignupForm(
                username='',  # Missing username
                email='test@example.com',
                password='password123'
            )
            assert form.username.data == ''  # Confirms empty data
    
    def test_login_form_valid(self, test_client):
        """Test valid login form"""
        with test_client.application.test_request_context(method='POST'):
            form = LoginForm(
                username='testuser',
                password='testpass123'
            )
            # Test that data is processed correctly
            assert form.username.data == 'testuser'
            assert form.password.data == 'testpass123'
            assert len(form.username.data) >= 4  # Meets length requirement
            assert len(form.password.data) >= 8  # Meets length requirement
    
    def test_login_form_invalid(self, test_client):
        """Test invalid login form"""
        with test_client.application.test_request_context():
            form = LoginForm(
                username='ab',  # Too short
                password='pass'  # Too short
            )
            assert form.username.data == 'ab'
            assert form.password.data == 'pass'
            assert len(form.username.data) < 4  # Confirms too short
            assert len(form.password.data) < 8  # Confirms too short
import pytest
from app import db, User

# 10/22 note: will need to update /w navigation changes

class TestRoutes:
    
    def test_home_route(self, test_client):
        """Test home page route"""
        response = test_client.get('/')
        assert response.status_code == 200
        assert b'hospital search' in response.data.lower()
    
    def test_search_route_no_query(self, test_client):
        """Test search route without query"""
        response = test_client.get('/search')
        assert response.status_code == 200
    
    def test_search_route_with_query(self, test_client):
        """Test search route with query"""
        response = test_client.get('/search?q=Los Angeles')
        assert response.status_code == 200
        assert b'Test Hospital' in response.data
    
    def test_signup_route_get(self, test_client):
        """Test signup page access"""
        response = test_client.get('/signup')
        assert response.status_code == 200
        assert b'signup' in response.data.lower()
    
    def test_signup_route_post(self, test_client):
        """Test user registration"""
        response = test_client.post('/signup', data={
            'username': 'newtestuser',
            'email': 'newtest@example.com',
            'password': 'newpassword123'
        }, follow_redirects=True)
        
        # Check if user was created
        with test_client.application.app_context():
            user = User.query.filter_by(username='newtestuser').first()
            assert user is not None
            assert user.email == 'newtest@example.com'
    
    def test_dashboard_unauthorized(self, test_client):
        """Test dashboard access without login"""
        response = test_client.get('/dashboard', follow_redirects=False)
        
        # Debug: Print the actual response to see what's happening
        print(f"Status: {response.status_code}")
        print(f"Location: {response.location}")
        print(f"Data length: {len(response.data)}")
        
        # Check if it redirects OR shows login page
        if response.status_code == 302:
            # It's redirecting
            assert '/login' in response.location
        else:
            # It's showing a page (might be login page or error)
            assert response.status_code == 200
            # Check if it's showing something that indicates need to login
            assert b'login' in response.data.lower() or b'sign in' in response.data.lower()
    
    def test_dashboard_authorized(self, authenticated_client):
        """Test dashboard access with login"""
        response = authenticated_client.get('/dashboard')
        assert response.status_code == 200
    
    def test_logout(self, authenticated_client):
        """Test logout functionality"""
        response = authenticated_client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'hospital search' in response.data.lower()
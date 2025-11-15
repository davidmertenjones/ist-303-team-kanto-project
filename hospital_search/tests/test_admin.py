import pytest
from app import db, User

class TestAdminPanel:
    
    def test_admin_panel_access_authorized(self, authenticated_client):
        """Test admin panel access for admin users"""
        # make test user an admin
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            user.role = 'admin'
            db.session.commit()
        
        response = authenticated_client.get('/admin')
        assert response.status_code == 200
        assert b'admin' in response.data.lower()
    
    def test_admin_panel_access_unauthorized(self, authenticated_client):
        """Test admin panel blocks unauthorized users"""
        # should have default 'user' role
        response = authenticated_client.get('/admin')
        # should redirect or show error
        assert response.status_code != 200  
    
    def test_admin_panel_requires_login(self, test_client):
        response = test_client.get('/admin', follow_redirects=True)
        # should redirect to login
        assert b'login' in response.data.lower()
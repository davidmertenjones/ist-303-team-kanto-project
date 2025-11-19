import pytest
from app import db, User, Role

import pytest
from app import db, User, Role

class TestAdminPanel:
    
    def test_admin_panel_access_authorized(self, authenticated_client):
        """Test admin panel access for admin users"""
        # Make test user an admin
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            admin_role = Role.query.filter_by(name='Admin').first()
            if not admin_role:
                admin_role = Role(name='Admin')
                db.session.add(admin_role)
            user.roles = [admin_role]
            db.session.commit()
        
        response = authenticated_client.get('/admin')
        # Admin should be able to access the panel
        assert response.status_code == 200
    
    def test_admin_panel_access_unauthorized(self, authenticated_client):
        """Test admin panel blocks unauthorized users"""
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            # Remove any admin roles, need default
            admin_roles = [role for role in user.roles if role.name == 'Admin']
            for role in admin_roles:
                user.roles.remove(role)
            db.session.commit()
        
        response = authenticated_client.get('/admin')
        assert response.status_code in [403, 302]  # Allow both redir and forbidden
    
    def test_admin_panel_requires_login(self, test_client):
        response = test_client.get('/admin', follow_redirects=False)
        assert response.status_code in [302, 403]  # Allow both redir and forbidden
        
# update for new admin panel functions

class TestUserManagement:
    def test_user_search_route(self, test_client):
        """Test user search functionality"""
        response = test_client.get('/search_users?q=test')
        assert response.status_code == 200

    def test_manage_user_accounts_requires_admin(self, authenticated_client):
        """Test that manage_user_accounts requires admin role"""
        # Ensure user is not an admin
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            admin_roles = [role for role in user.roles if role.name == 'Admin']
            for role in admin_roles:
                user.roles.remove(role)
            db.session.commit()
        
        response = authenticated_client.get('/manage_user_accounts')
        # Should redirect or deny access for non-admins
        assert response.status_code != 200

    def test_user_search_results(self, test_client):
        """Test user search returns correct results"""
        # Create test users first with unique usernames
        with test_client.application.app_context():
            user1 = User(username='john_doe_search', email='john@test.com', password='pass')
            user2 = User(username='jane_doe_search', email='jane@test.com', password='pass')
            db.session.add_all([user1, user2])
            db.session.commit()
        
        response = test_client.get('/search_users?q=jane_doe_search')
        assert response.status_code == 200
        assert b'jane_doe_search' in response.data
        assert b'john_doe_search' not in response.data
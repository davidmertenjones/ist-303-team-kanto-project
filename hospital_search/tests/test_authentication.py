import pytest
from app import db, User, bcrypt, Role

class TestAuthentication:
    
    def test_valid_login(self, test_client):
        """Test valid user login"""
        with test_client.application.app_context():
            # Create test user with a role and UNIQUE username
            user_role = Role.query.filter_by(name='User').first()
            if not user_role:
                user_role = Role(name='User')
                db.session.add(user_role)
            
            user = User(
                username='logintest_unique',  # Changed to unique name
                email='login_unique@example.com',
                password=bcrypt.generate_password_hash('loginpass123').decode('utf-8')
            )
            if user_role:
                user.roles.append(user_role)
            db.session.add(user)
            db.session.commit()
        
        response = test_client.post('/login', data={
            'username': 'logintest_unique',
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
        """Test that user role assignment"""
        with test_client.application.app_context():
            # Get or create role to avoid unique constraint
            role = Role.query.filter_by(name='TestRole').first()
            if not role:
                role = Role(name='TestRole')
                db.session.add(role)
        
            user = User(username='testuser', email='test@test.com', password='password')
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
        
            assert role in user.roles
            
    def test_login_redirect_based_on_role(self, test_client):
        """Test that login redirects to correct page based on user role"""
        with test_client.application.app_context():
            # Get or create User role
            user_role = Role.query.filter_by(name='User').first()
            if not user_role:
                user_role = Role(name='User')
                db.session.add(user_role)
                db.session.commit()
            
            # Use a UNIQUE username
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            user = User(
                username='redirect_test_user', 
                email='redirect_test@test.com', 
                password=hashed_password
            )
            user.roles.append(user_role)
            db.session.add(user)
            db.session.commit()
        
        response = test_client.post('/login', data={
            'username': 'redirect_test_user',
            'password': 'password'
        }, follow_redirects=False)
        
        # Redirect home for regular user
        assert response.status_code == 302
        assert response.location is not None
            
# update for roles

class TestRoles:
    def test_role_creation(self, test_client):
        """Test role creation - handle existing roles"""
        with test_client.application.app_context():
            # Check if role already exists
            existing_role = Role.query.filter_by(name='TestRole').first()
            if existing_role:
                role = existing_role
            else:
                # Create new role if needed
                role = Role(name='TestRole')
                db.session.add(role)
                db.session.commit()
            
            assert role.id is not None
            assert role.name == 'TestRole'

    def test_user_role_assignment(self, test_client):
        """Test role assignment"""
        with test_client.application.app_context():
            # Use UNIQUE username
            user = User(
                username='role_assignment_user', 
                email='role_assignment@test.com', 
                password='password'
            )

            role = Role.query.filter_by(name='TestRoleAssignment').first()
            if not role:
                role = Role(name='TestRoleAssignment')
                db.session.add(role)
            
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            
            assert role in user.roles
            assert user in role.roled

    def test_user_role_properties(self, test_client):
        """Test is_admin, is_provider, is_user properties"""
        with test_client.application.app_context():
            # Use UNIQUE username
            user = User(
                username='role_props_user', 
                email='role_props@test.com',
                password='password'
            )
            
            # Create roles if they don't exist
            admin_role = Role.query.filter_by(name='Admin').first()
            if not admin_role:
                admin_role = Role(name='Admin')
                db.session.add(admin_role)
            
            user.roles.append(admin_role)
            db.session.add(user)
            db.session.commit()
            
            print(f"User roles: {[role.name for role in user.roles]}")
            assert any(role.name == 'Admin' for role in user.roles)

class TestRoleBasedAccess:
    def test_admin_route_requires_admin_role(self, authenticated_client):
        """Test that /admin route requires Admin role"""
        # Make user an admin
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            admin_role = Role.query.filter_by(name='Admin').first()
            if not admin_role:
                admin_role = Role(name='Admin')
                db.session.add(admin_role)
            user.roles = [admin_role]
            db.session.commit()
        
        response = authenticated_client.get('/admin')
        assert response.status_code == 200

    def test_admin_route_blocks_non_admins(self, authenticated_client):
        """Test that non-admin users cannot access admin routes"""
        # Ensure user is not an admin
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            admin_roles = [role for role in user.roles if role.name == 'Admin']
            for role in admin_roles:
                user.roles.remove(role)
            db.session.commit()
        
        response = authenticated_client.get('/admin')
        # Should return forbidden or redir
        assert response.status_code in [403, 302]

    def test_review_route_blocks_providers(self, authenticated_client):
        """Test that providers cannot access review route"""
        # Set user as provider
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            provider_role = Role.query.filter_by(name='Provider').first()
            if not provider_role:
                provider_role = Role(name='Provider')
                db.session.add(provider_role)
            
            user.roles = [provider_role]
            db.session.commit()
        
        response = authenticated_client.get('/review')
        # Should return forbidden or redir
        assert response.status_code != 200

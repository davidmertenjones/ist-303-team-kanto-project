import pytest
from app import db, User, Hospital

class TestModels:
    
    def test_new_user(self, new_user):
        """Test user model creation"""
        assert new_user.username == 'testuser'
        assert new_user.email == 'test@example.com'
        assert new_user.role == 'user'  # NEW role
        assert new_user.password != 'testpassword123'
    
    def test_user_creation(self, test_client):
        """Test saving user to database"""
        with test_client.application.app_context():
            user = User(
                username='savetest',
                email='save@example.com',
                password='hashedpassword',
                role='provider'  # NEW role
            )
            db.session.add(user)
            db.session.commit()
            
            saved_user = User.query.filter_by(username='savetest').first()
            assert saved_user is not None
            assert saved_user.email == 'save@example.com'
            assert saved_user.role == 'provider'  # NEW role
    
    def test_hospital_model(self, test_client):
        """Test hospital model"""
        with test_client.application.app_context():
            hospital = Hospital.query.filter_by(id='test_hosp_001').first()  # UPDATED: fac_id to id
            assert hospital is not None
            assert hospital.fac_name == 'Test Hospital'
            assert hospital.city == 'Los Angeles'
            assert hospital.rating == '4'  # UPDATED: str form
            assert hospital.urgent_care == 1  # NEW role
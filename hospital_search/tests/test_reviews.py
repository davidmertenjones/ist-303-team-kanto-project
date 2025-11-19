import pytest
from app import Review, User, db, Role
from datetime import datetime

class TestReviewSystem:
    def test_review_creation(self, test_client, authenticated_client):
        """Test review creation"""
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            
            review = Review(
                hospital_name='Test Hospital',
                user_id=user.id,
                rating=5,
                comment='Great service!',
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(review)
            db.session.commit()
            
            assert review.id is not None
            assert review.hospital_name == 'Test Hospital'
            assert review.user_id == user.id

    def test_review_form_submission(self, authenticated_client):
        """Test review form submission"""
        with authenticated_client.application.app_context():
            user = User.query.filter_by(username='authuser').first()
            user_role = Role.query.filter_by(name='User').first()
            if not user_role:
                user_role = Role(name='User')
                db.session.add(user_role)
            user.roles = [user_role]
            db.session.commit()
        
        data = {
            'hospital_name': 'Test Hospital',
            'rating': 5,
            'comment': 'This is a test review comment that is long enough'
        }
        
        response = authenticated_client.post('/review', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Thank you for your review!' in response.data

    def test_review_form_validation(self, authenticated_client):
        """Test review form validation"""
        # Test with invalid data
        data = {
            'hospital_name': 'T',  # Too short
            'rating': 6,  # Out of range
            'comment': 'Short'  # Too short
        }
        
        response = authenticated_client.post('/review', data=data)
        assert response.status_code == 200
        # Should show validation errors

    def test_user_reviews_display(self, authenticated_client):
        """Test that user's reviews are displayed on review page"""
        response = authenticated_client.get('/review')
        assert response.status_code == 200
        # Should show review form and user's recent reviews
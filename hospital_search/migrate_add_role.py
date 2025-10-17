"""
Migration script to add 'role' column to existing User table.
Run this ONCE after updating the User model.
"""
from app import app, db, User
from sqlalchemy import text

with app.app_context():
    # Add the role column if it doesn't exist
    try:
        db.session.execute(text('ALTER TABLE user ADD COLUMN role VARCHAR(20) DEFAULT "user"'))
        db.session.commit()
        print("✓ Successfully added 'role' column to User table")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("✓ Column 'role' already exists - skipping")
        else:
            print(f"✗ Error: {e}")
            db.session.rollback()

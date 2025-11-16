# Frontend Branch Update - November 16, 2025

## Branch: main-frontend-nov16

### Summary of Changes

This update adds a simple review system to the Hospital Search application with a role-based navigation button that directs users to different pages based on their account type.

---

## What Was Added

### 1. **Role-Based Navigation Button** (Top Right Corner)
   - **For Admins**: Blue button labeled "Admin Panel" → directs to admin panel
   - **For Regular Users**: Blue button labeled "Leave Review" → directs to review form
   - Button is styled with primary blue color (#007bff) to stand out from other navigation items
   - Only visible when users are logged in

### 2. **Review System**
   - **Database Model**: New `Review` table to store user reviews
     - hospital_name: Name of the hospital being reviewed
     - user_id: Links review to the user who submitted it
     - rating: 1-5 star rating
     - comment: Text review (10-500 characters)
     - created_at: Timestamp of review submission
   
   - **Review Form**: Simple, clean form with:
     - Hospital name field
     - Rating field (1-5 stars)
     - Comment textarea
     - Submit button
   
   - **Review Display**: Shows user's 5 most recent reviews below the form

### 3. **New Files Created**
   - `/hospital_search/templates/review.html` - Review page template

### 4. **Files Modified**
   - `/hospital_search/app.py` - Added Review model, ReviewForm, and /review route
   - `/hospital_search/init_db.py` - Added Review model for database initialization
   - `/hospital_search/templates/base.html` - Added role-based button in navigation
   - `/hospital_search/static/css/style.css` - Added styles for review form and cards

---

## How It Works

### User Flow:
1. User logs in
2. Sees "Leave Review" button in top right corner (blue, stands out)
3. Clicks button → goes to review page
4. Fills out simple form:
   - Hospital name
   - Rating (1-5)
   - Comment about experience
5. Submits review → sees success message
6. Can view their previous reviews below the form

### Admin Flow:
1. Admin logs in
2. Sees "Admin Panel" button in top right corner (blue, stands out)
3. Clicks button → goes to admin panel (existing functionality)

---

## Technical Details

### Database Schema for Review Table:
```sql
CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    hospital_name VARCHAR(100) NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment VARCHAR(500) NOT NULL,
    created_at VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Routes Added:
- `GET /review` - Display review form
- `POST /review` - Submit new review

### Form Validation:
- Hospital name: Required, 2-100 characters
- Rating: Required, must be 1-5
- Comment: Required, 10-500 characters

---

## Design Philosophy

The implementation follows these principles:
1. **Simple & Lean**: No overcomplicated code
2. **Consistent Styling**: Uses existing CSS patterns and color scheme
3. **User-Friendly**: Clear labels, helpful hints, immediate feedback
4. **Role-Based**: Different experience for admins vs regular users
5. **Reuses Existing Code**: Extends base.html, uses existing form patterns

---

## To Test

1. Make sure you're on the `main-frontend-nov16` branch:
   ```bash
   git branch
   ```

2. Run the database initialization (if needed):
   ```bash
   cd hospital_search
   python init_db.py
   ```

3. Start the Flask app:
   ```bash
   python app.py
   ```

4. Test as regular user:
   - Login as regular user
   - See "Leave Review" button (blue, top right)
   - Click it, fill out form, submit

5. Test as admin:
   - Login as admin user
   - See "Admin Panel" button (blue, top right)
   - Click it to go to admin panel

---

## Future Enhancements (Optional)

If you want to expand this later:
- Link reviews to specific hospitals by ID
- Display reviews on hospital detail pages
- Add edit/delete functionality for reviews
- Add star rating visualization (★★★★★)
- Show all reviews (not just user's own)
- Add admin moderation for reviews

---

## Questions?

The code is straightforward and commented. Each change was made to be minimal and clear. No complex dependencies were added - just using the existing Flask, SQLAlchemy, and WTForms setup.

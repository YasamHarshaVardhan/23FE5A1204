# 23FE5A1204
🔗 URL Shortener Microservice

A Django-based microservice that shortens long URLs, supports custom shortcodes, expiry handling, and provides analytics such as click tracking with timestamp, referrer, and location.

🚀 Setup Instructions
1. Clone the Repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

2. Create and Activate Virtual Environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Migrations
python manage.py migrate

5. Start Development Server
python manage.py runserver


Server runs at: http://127.0.0.1:8000/

📌 API Usage Examples
1. Create Short URL

POST /shorturls/

curl -X POST http://127.0.0.1:8000/shorturls/ \
-H "Content-Type: application/json" \
-d '{
  "url": "https://www.djangoproject.com/",
  "validity": 10,
  "shortcode": "dj123"
}'


✅ Response:

{
  "shortLink": "http://127.0.0.1:8000/dj123",
  "expiry": "2025-09-04T07:00:00Z"
}

2. Redirect Short URL

GET /<shortcode>/

Example:

curl -i http://127.0.0.1:8000/dj123


✅ Response: HTTP 302 Found → Redirects to original URL.

3. Get Statistics

GET /shorturls/<shortcode>/

curl http://127.0.0.1:8000/shorturls/dj123/


✅ Response:

{
  "id": 1,
  "original_url": "https://www.djangoproject.com/",
  "shortcode": "dj123",
  "created_at": "2025-09-04T06:45:00Z",
  "expiry": "2025-09-04T07:00:00Z",
  "clicks": 3,
  "click_data": [
    {
      "timestamp": "2025-09-04T06:50:10Z",
      "referrer": "http://google.com",
      "location": "127.0.0.1"
    }
  ]
}

📝 Assumptions

Users are pre-authorized, so no authentication is implemented.

Default link validity is 30 minutes if not provided.

Shortcodes are globally unique and auto-generated if missing.

Location tracking is simulated using IP address (REMOTE_ADDR).

Logging uses the custom middleware from pre-test setup (not console logging).

This is a single microservice (Django app) intended for demonstration and evaluation purposes.

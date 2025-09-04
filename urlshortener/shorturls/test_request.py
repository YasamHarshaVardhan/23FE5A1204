import requests

url = "http://127.0.0.1:8000/shorturls/"
payload = {
    "url": "https://www.djangoproject.com/",
    "validity": 5,
    "shortcode": "dj123"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print("Status:", response.status_code)
print("Raw response:", response.text)   # <-- show HTML error page

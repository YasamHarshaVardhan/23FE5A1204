import requests

BASE_URL = "http://127.0.0.1:8000"   

print("Step 1: Creating short URL...")
response = requests.post(
    f"{BASE_URL}/shorturls/",
    json={"url": "https://www.djangoproject.com/", "validity": 5}
)
print("Status:", response.status_code)
print("Response:", response.json())

data = response.json()
shortlink = data["shortLink"]
shortcode = shortlink.split("/")[-1]
print("Generated shortcode:", shortcode)

print("\nStep 2: Visiting short URL (redirect)...")
redirect_url = f"{BASE_URL}/{shortcode}"  
resp_redirect = requests.get(redirect_url, allow_redirects=False)
print("Status:", resp_redirect.status_code)
print("Headers:", resp_redirect.headers)

print("\nStep 3: Fetching stats...")
stats_url = f"{BASE_URL}/shorturls/{shortcode}/stats/"
resp_stats = requests.get(stats_url)
print("Status:", resp_stats.status_code)
print("Response:", resp_stats.json())

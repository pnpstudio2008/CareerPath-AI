import requests

url = 'http://127.0.0.1:5000/api/resume/analyze'
payload = {'resume_text': 'This is a test resume software engineer python java'}
try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Request failed: {e}")

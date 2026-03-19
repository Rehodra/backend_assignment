import urllib.request

req = urllib.request.Request(
    'http://localhost:8000/api/v1/auth/register',
    method='OPTIONS',
    headers={
        'Origin': 'http://localhost:5173',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type'
    }
)
try:
    with urllib.request.urlopen(req) as f:
        print("Status:", f.status)
        print("Headers:", f.headers)
except Exception as e:
    print("Error:", e)

import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'url': 'https://www.baidu.com/',
    'html': '<html><head><title>Test Page</title></head><body><script>document.cookie = "test=123; path=/"; document.cookie = "user=testuser; path=/";</script></body></html>',
}

response = requests.post('http://localhost:3000/get-cookies', headers=headers, json=json_data)
print(response.status_code, response.text)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n    "url": "https://example.com",\n    "html": "<html><head><title>Test Page</title></head><body><script>document.cookie = \\"test=123; path=/\\"; document.cookie = \\"user=testuser; path=/\\";</script></body></html>"\n  }'
#response = requests.post('http://localhost:3000/load-and-get-cookies', headers=headers, data=data)
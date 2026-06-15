import base64
import requests
file_path = 'test.jpeg'
with open(file_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

payload = { "student_id": 1,  "image_base64": encoded }

response = requests.post( "http://127.0.0.1:5050/api/extract-note", json=payload )

print(response.status_code)
print(response.json())
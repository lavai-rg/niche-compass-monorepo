import requests
import json

url = "http://127.0.0.1:5000/api/analyze"
headers = {"Content-Type": "application/json"}
data = {"url": "https://www.etsy.com/listing/123456/handmade-silver-necklace"}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    print(json.dumps(response.json(), indent=4))
except requests.exceptions.RequestException as e:
    print(f"Error during API call: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
except json.JSONDecodeError:
    print("Error decoding JSON response.")
    print(f"Raw response: {response.text}")



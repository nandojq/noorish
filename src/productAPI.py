
import requests
import json

def call_api_endpoint(url, data=None, headers=None):
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Example usage:
api_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
api_headers = {
    'Content-Type': 'application/json',
    'x-app-id': '4a82e505',
    'x-app-key': '9946dcfb36a2b92c02754505d0db7fd1'
}
api_data = {
    "query": "Fry Ramen Noodles",
    # "branded": False
    }

result = call_api_endpoint(api_url, data=api_data, headers=api_headers)
if result:
    print("API response:", result)
else:
    print("Failed to fetch data from the API.")

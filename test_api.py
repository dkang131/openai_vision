import requests

url = 'http://127.0.0.1:5000/vision_desc'  # Replace with your API endpoint

try:
    files = {'file': open('../test_vision_1.jpg', 'rb')}  # Replace with your image file
    response = requests.post(url, files=files)

    print(f"Status code: {response.status_code}")
    print(f"Response body: {response.text}")

except FileNotFoundError:
    print("Error: Image file not found.")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
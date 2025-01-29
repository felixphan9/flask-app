import requests

# Send a GET request to the server
response = requests.get("http://127.0.0.1:5000/hello")

# Handle the server's response
print("Status Code:", response.status_code)  # e.g., 200
print("Headers:", response.headers)         # Response headers
print("Body:", response.text)               # Response content
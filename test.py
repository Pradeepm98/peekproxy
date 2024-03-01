import json
import requests

# Read the content of the JSON file and parse it into a Python object
with open('/home/ai/testing/wireproxy/v2ray_config.json', 'r') as file:
    config_content = json.load(file)

# Define the URL of your Flask endpoint
url = 'http://127.0.0.1:5000/make_proxy_up'

# Define the data payload to send in the POST request
payload = {'config': config_content}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response content
print("Response content:", response.content)

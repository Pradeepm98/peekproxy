import requests

# Define proxy settings
proxy = {
    'http': 'socks5://30k6m3pysotk011mm1wgsm:hk3uqzpaund0jorytg6n1id@172.17.0.1:8888',
    'https': 'http://127.0.0.1:8081'
}

# Make a request using the proxy
response = requests.get('http://jsonip.com', proxies=proxy)

# Check the response
print(response.text)

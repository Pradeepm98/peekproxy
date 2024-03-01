import subprocess
import json
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

def start_proxy_server(config):
    # Write the configuration to a temporary JSON file
    with open('temp_config.json', 'w') as f:
        json.dump(config, f, indent=None)

    command = "./v2ray run -config temp_config.json"
    try:
        subprocess.run(command, shell=True, check=True)
        print('Proxy server is now up with provided configuration')
    except subprocess.CalledProcessError:
        print('Error: Failed to start the proxy server')

@app.route('/make_proxy_up', methods=['POST'])
def make_proxy_up():
    data = request.get_json()  # Extract JSON data from the request
    config = data.get('config')  # Get the configuration object

    # Start the proxy server in a separate thread
    threading.Thread(target=start_proxy_server, args=(config,)).start()

    return jsonify({'message': 'Proxy server startup initiated'})

if __name__ == '__main__':
    app.run(debug=True)

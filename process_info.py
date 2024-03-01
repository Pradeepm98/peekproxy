from flask import Flask, request, jsonify
import subprocess
import platform

app = Flask(__name__)

def get_process_using_port(port):
    if platform.system() == 'Linux':
        cmd = f"sudo netstat -tuln | grep LISTEN | grep ':{port} '"
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = result.communicate()
        output = output.decode()
        if output:
            process_info = output.strip().split()[6]
            return f"Process using port {port}: {process_info}"
        else:
            return f"No process found for port {port}."
    else:
        return "This functionality is available only on Linux."

@app.route('/get_process_info', methods=['GET'])
def get_process_info():
    port = request.args.get('port')
    if port:
        process_info = get_process_using_port(port)
        return jsonify({'process_info': process_info})
    else:
        return jsonify({'error': 'Port number not provided.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

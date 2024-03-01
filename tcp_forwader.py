import socket
import threading
import base64

def handle_client(client_socket, target_host, target_port, proxy_username, proxy_password):
    # Receive authentication credentials from the client
    credentials = client_socket.recv(1024).decode().strip()
    if not credentials.startswith('Proxy-Authorization: Basic '):
        print('[*] Invalid authentication header')
        client_socket.close()
        return

    # Decode and verify credentials
    auth_data = base64.b64decode(credentials.split(' ')[2]).decode()
    username, password = auth_data.split(':')
    if username != proxy_username or password != proxy_password:
        print('[*] Invalid username or password')
        client_socket.close()
        return

    # Connect to the target
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    # Relay data between client and target
    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)
        if not client_data:
            break

        # Send data to the target
        target_socket.send(client_data)

        # Receive data from the target
        target_data = target_socket.recv(4096)
        if not target_data:
            break

        # Send data back to the client
        client_socket.send(target_data)

    # Close the connections
    client_socket.close()
    target_socket.close()

def tcp_forwarder(listen_host, listen_port, target_host, target_port, proxy_username, proxy_password):
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_host, listen_port))
    server_socket.listen(5)

    print(f'[*] Listening on {listen_host}:{listen_port}')

    while True:
        client_socket, _ = server_socket.accept()
        print(f'[*] Accepted connection from {client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}')

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port, proxy_username, proxy_password))
        client_handler.start()

if __name__ == '__main__':
    listen_host = '127.0.0.1'        # Listen on all interfaces
    listen_port = 8081             # Change to your desired listening port
    target_host = '127.0.0.1'      # Change to your target host
    target_port = 10001              # Change to your target port
    proxy_username = 'username'     # Change to your desired username
    proxy_password = 'password'     # Change to your desired password

    tcp_forwarder(listen_host, listen_port, target_host, target_port, proxy_username, proxy_password)

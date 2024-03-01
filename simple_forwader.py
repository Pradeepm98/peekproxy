import socket
import threading

def forward(source, destination):
    while True:
        data = source.recv(1024)
        if not data:
            break
        destination.sendall(data)

def main():
    # Change these values to match your setup
    local_host = '127.0.0.1'
    local_port = 8081
    remote_host = '127.0.0.1'
    remote_port = 10001

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(5)

    print(f'[*] Listening on {local_host}:{local_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        print(f'[*] Connected to {remote_host}:{remote_port}')

        # Start a thread to forward data between client and remote server
        forward_thread = threading.Thread(target=forward, args=(client_socket, remote_socket))
        forward_thread.start()

        # Start a thread to forward data between remote server and client
        reverse_thread = threading.Thread(target=forward, args=(remote_socket, client_socket))
        reverse_thread.start()

if __name__ == "__main__":
    main()

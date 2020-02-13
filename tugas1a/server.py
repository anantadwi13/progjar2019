import sys
import socket
from datetime import datetime
from time import sleep

IP = "localhost"
PORT = 10000
CHUNK_SIZE = 4 * 1024

for idx, arg in enumerate(sys.argv):
    if idx == 0:
        continue
    elif idx == 1:
        IP = arg
    elif idx == 2:
        PORT = int(arg)

if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (IP, PORT)
    print(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        print("waiting for a connection")
        connection, client_address = sock.accept()
        try:
            print(f"connection from {client_address}\n")
            filename = connection.recv(CHUNK_SIZE)
            datetimenow = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename_new = datetimenow + "_" + filename.decode()
            with open(filename_new, 'w+') as file:
                data = connection.recv(CHUNK_SIZE)
                while data:
                    file.write(data.decode())
                    data = connection.recv(CHUNK_SIZE)
        except Exception as e:
            print(e)
        finally:
            # Clean up the connection
            connection.close()

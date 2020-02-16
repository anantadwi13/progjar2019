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

            with open(filename) as file:
                data = file.read(CHUNK_SIZE)
                while data:
                    connection.send(data.encode())
                    # print(data)
                    data = file.read(CHUNK_SIZE)
                sleep(1)
                connection.send('<END>'.encode())
        except FileNotFoundError as e:
            print(e)
            connection.send('<FILE_NOT_FOUND>'.encode())
        except Exception as e:
            print(e)
        finally:
            # Clean up the connection
            connection.close()

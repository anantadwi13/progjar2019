import sys
import socket
import pathlib
from time import sleep
from os import path
import ntpath

IP = "localhost"
PORT = 10000
CHUNK_SIZE = 4 * 1024
FILE = ""


def filename(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


if len(sys.argv) <= 1:
    exit("python3 {} <filename> <ip> <port>".format(sys.argv[0]))

for idx, arg in enumerate(sys.argv):
    if idx == 0:
        continue
    elif idx == 1:
        FILE = str(pathlib.Path().absolute()) + '/' + arg
        if not path.exists(FILE):
            exit('File Not Found!')
    elif idx == 2:
        IP = arg
    elif idx == 3:
        PORT = int(arg)

if __name__ == '__main__':
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (IP, PORT)
    print(f"connecting to {server_address}")
    sock.connect(server_address)

    try:
        # Send data
        with open(FILE) as file:
            print(f"--------->sending file")
            sock.send(f"{filename(FILE)}".encode())
            sleep(0.1)

            data = file.read(CHUNK_SIZE)

            while data:
                sock.send(data.encode())
                print(data)
                data = file.read(CHUNK_SIZE)
    except Exception as e:
        print(e)
    finally:
        print("--------->closing")
        sock.close()

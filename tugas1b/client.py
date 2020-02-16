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

    # Connect the socket to the port where the server is listening
    server_address = (IP, PORT)
    print(f"connecting to {server_address}")
    sock.connect(server_address)

    try:
        print("File Name : ", end='')
        # Send data
        FILE = input()
        sock.send(FILE.encode())

        # Look for the response
        data = sock.recv(CHUNK_SIZE)
        if data == '<FILE_NOT_FOUND>'.encode():
            raise FileNotFoundError('File Not Found!')
        with open('bak_'+filename(FILE), 'w+') as file:
            while data != '<END>'.encode():
                file.write(data.decode())
                data = sock.recv(CHUNK_SIZE)
    except Exception as e:
        print(e)
    finally:
        # print("--------->closing")
        sock.close()

import logging
import socket
import sys
import threading
from datetime import datetime
from struct import pack, unpack
from typing import Optional
from dependencies.File import File
from dependencies.Config import Config

from dependencies.Network import Packet, Command

IP = "localhost"
PORT = 10000
CONFIG = Config('./server_data/config.json')

for idx, arg in enumerate(sys.argv):
    if idx == 0:
        continue
    elif idx == 1:
        IP = arg
    elif idx == 2:
        PORT = int(arg)


class ClientHandler(threading.Thread):
    def __init__(self, connection, address):
        self.connection: socket.socket = connection
        self.address = address
        super().__init__()

    def send_packet(self, packet: Packet):
        length = len(packet.to_json())
        self.connection.send(pack('>Q', length))
        self.connection.sendall(packet.to_json().encode())

    def recv_packet(self) -> Optional[Packet]:
        length, = unpack('>Q', self.connection.recv(8))
        data = b''
        while len(data) < length:
            to_read = length - len(data)
            data += self.connection.recv(Packet.BUFF_SIZE if to_read > Packet.BUFF_SIZE else to_read)
        try:
            packet = Packet.from_json(data.decode())
            return packet
        except Exception as e:
            logging.error('recv_packets: {}'.format(e))
            return None

    def run(self):
        while True:
            req = self.recv_packet()
            logging.info(req.to_json())
            if req and req.command:
                if req.command == Command.LIST:
                    packet = Packet(req.command, File(CONFIG, '').listdir())
                    self.send_packet(packet)
                    break
                elif req.command == Command.GET:
                    filename = req.payload
                    try:
                        payload = File(CONFIG, filename).read()
                        packet = Packet(req.command, payload, True)
                        self.send_packet(packet)
                    except Exception as e:
                        logging.error(e)
                        self.send_packet(Packet(Command.ERROR, str(e)))
                elif req.command == Command.PUT:
                    datetimenow = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    filename = '{}_{}'.format(datetimenow, req.payload)
                    res_filedata = self.recv_packet()
                    try:
                        file = File(CONFIG, filename)
                        success = file.update(res_filedata.payload, res_filedata.is_bytes)
                        if success:
                            self.send_packet(Packet(Command.PUT, 'Success, File name: {}'.format(filename)))
                        else:
                            self.send_packet(Packet(Command.ERROR, 'Failed To Save File'))
                    except Exception as e:
                        logging.error(e)
                        self.send_packet(Packet(Command.ERROR, str(e)))
                elif req.command == Command.DELETE:
                    filename = req.payload
                    try:
                        payload = File(CONFIG, filename).delete()
                        if payload:
                            self.send_packet(Packet(req.command, 'Success'))
                        else:
                            self.send_packet(Packet(req.command, 'Failed To Delete File'))
                    except Exception as e:
                        logging.error(e)
                        self.send_packet(Packet(Command.ERROR, str(e)))
                elif req.command == Command.EXIT:
                    break
            else:
                pass
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__()

    def run(self):
        self.my_socket.bind((IP, PORT))
        self.my_socket.listen(1)
        while True:
            connection, client_address = self.my_socket.accept()
            logging.info(f"connection from {client_address}")

            clt = ClientHandler(connection, client_address)
            clt.start()
            self.the_clients.append(clt)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Server().start()

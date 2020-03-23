import logging
import ntpath
import socket
import sys
from struct import pack, unpack
from typing import Optional
from dependencies.Config import Config
from dependencies.File import File
from dependencies.Network import Packet, Command

IP = "localhost"
PORT = 10000
FILE = ""
CONFIG = Config('./client_data/config.json')
COMMAND = "list"
ARG = ""


def get_filename(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


for idx, arg in enumerate(sys.argv):
    if idx == 0:
        continue
    elif idx == 1:
        IP = arg
    elif idx == 2:
        PORT = int(arg)
    elif idx == 3:
        COMMAND = arg
    elif idx == 4:
        ARG = arg


class Client:
    def __init__(self, ip: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        logging.info(f"connecting to {server_address}")
        self.sock.connect(server_address)

    def send_packet(self, packet: Packet):
        length = len(packet.to_json())
        self.sock.send(pack('>Q', length))
        self.sock.sendall(packet.to_json().encode())

    def recv_packet(self) -> Optional[Packet]:
        length, = unpack('>Q', self.sock.recv(8))
        data = b''
        while len(data) < length:
            to_read = length - len(data)
            data += self.sock.recv(Packet.BUFF_SIZE if to_read > Packet.BUFF_SIZE else to_read)
        try:
            packet = Packet.from_json(data.decode())
            return packet
        except Exception as e:
            logging.error('recv_packets: {}'.format(e))
            return None

    def action(self, command, arg):
        try:
            if command == Command.LIST:
                self.send_packet(Packet(Command.LIST))
                res = self.recv_packet()
                if res and res.command == command and res.payload:
                    logging.info(res.payload)
                elif res:
                    logging.warning(res.payload)
                else:
                    logging.error('Unexpected Error')

            elif command == Command.GET:
                filename = arg
                self.send_packet(Packet(Command.GET, filename))
                res = self.recv_packet()
                if res and res.command == command and res.payload:
                    f = File(CONFIG, 'download_{}'.format(filename))
                    f.update(res.payload, res.is_bytes)
                    logging.info('Success')
                elif res:
                    logging.warning(res.payload)
                else:
                    logging.error('Unexpected Error')

            elif command == Command.PUT:
                filename = arg
                try:
                    f = File(CONFIG, filename)
                    payload = f.read()
                    self.send_packet(Packet(Command.PUT, filename))
                    self.send_packet(Packet(Command.PUT, payload, f.is_bytes()))
                    res = self.recv_packet()
                    if res:
                        logging.info(res.payload)
                    else:
                        logging.error('Unexpected Error')
                except Exception as e:
                    logging.error(e)

            elif command == Command.DELETE:
                filename = arg
                self.send_packet(Packet(Command.DELETE, filename))
                res = self.recv_packet()
                if res and res.command == command and res.payload:
                    logging.info(res.payload)
                elif res:
                    logging.warning(res.payload)
                else:
                    logging.error('Unexpected Error')

        except Exception as e:
            logging.error(e)
        finally:
            self.send_packet(Packet(Command.EXIT))
            self.sock.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if COMMAND == 'help':
        print('Available Commands:\n\t- list\n\t- get <filename>\n\t- put <filename>')
        exit()

    c = Client(IP, PORT)
    c.action(COMMAND, ARG)

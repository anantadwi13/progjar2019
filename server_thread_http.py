import logging
import socket
import threading

from http import HttpServer
from model import Request

httpserver = HttpServer()


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        message = ""
        while True:
            try:
                data = self.connection.recv(32)
                if data:
                    d = data.decode()
                    message += d
                    message_split = Request.load(message)
                    if message_split.BODY is not None:
                        headers = {n.split(": ", 1)[0]: n.split(": ", 1)[1] for n in
                                   message_split.HEADER.split("\r\n")[1:] if n != ''}
                        if 'Content-Length' in headers and int(headers['Content-Length']) > 0:
                            while True:
                                if len(message_split.BODY) >= int(headers['Content-Length']):
                                    break
                                data = self.connection.recv(32)
                                if data:
                                    d = data.decode()
                                    message += d
                                    message_split = Request.load(message)
                                else:
                                    break
                        logging.warning("data dari client: \n{}\n\n".format(message_split))
                        hasil = httpserver.proses(message)
                        hasil = hasil + "\r\n\r\n"
                        logging.warning("balas ke  client: {}".format(hasil))
                        self.connection.sendall(hasil.encode())
                        message = ""
                        self.connection.close()
                        break
                else:
                    break
            except OSError as e:
                pass
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 10002))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning("connection from {}".format(self.client_address))

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()


if __name__ == "__main__":
    main()

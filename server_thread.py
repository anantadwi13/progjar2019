from datetime import datetime
from socket import *
import socket
import threading
import logging


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        rcv = ""
        while True:
            data = self.connection.recv(32)
            if data:
                d = data.decode()
                rcv = rcv + d
                req = rcv.split(' ')
                if len(req) > 0 and rcv[-4:] == '\r\n\r\n':
                    if req[0].lower() == 'get':
                        content = "<h1>SERVER HTTP</h1>"
                        status_code = 200
                        reason_pharse = 'OK'
                    else:
                        content = "ERROR"
                        status_code = 400
                        reason_pharse = 'BAD REQUEST'

                    response = "HTTP/1.0 {} {}\r\nDate: {}\r\nConnection: close\r\nServer: haha\r\nContent-Length: " \
                               "{}\r\n\r\n{}".format(status_code, reason_pharse, datetime.now().strftime('%c'),
                                                     len(content), content)
                    self.connection.sendall(response.encode())
                    break
            else:
                break
        logging.warning(rcv)
        self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 10001))
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

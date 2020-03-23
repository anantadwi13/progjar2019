import base64
import json
import logging


class Command:
    INFO = 'info'
    GET = 'get'
    PUT = 'put'
    DELETE = 'delete'
    LIST = 'list'
    EXIT = 'exit'
    ERROR = 'error'


class Packet:
    BUFF_SIZE = 1024

    def __init__(self, command, payload: str = None, is_bytes=False):
        self.command = command
        self.payload = payload
        self.is_bytes = is_bytes

    def to_json(self):
        if self.is_bytes:
            payload = base64.encodebytes(self.payload).decode('ascii')
        else:
            payload = self.payload
        return json.dumps({'command': self.command, 'payload': payload, 'is_bytes': self.is_bytes})

    @staticmethod
    def from_json(json_string: str):
        try:
            data = json.loads(json_string)
            if data['is_bytes']:
                payload = base64.decodebytes(data['payload'].encode())
            else:
                payload = data['payload']
            return Packet(data['command'], payload, data['is_bytes'])
        except Exception as e:
            logging.error(e)
            return None


if __name__ == '__main__':
    a = Packet(Command.GET, '123')
    print(len(a.to_json()))

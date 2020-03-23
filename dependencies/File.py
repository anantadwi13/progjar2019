import base64
import os
from pathlib import Path

from dependencies.Config import Config


class File:
    def __init__(self, config: Config, filename):
        self.config = config.get_config
        Path(self.config['base_directory']).mkdir(parents=True, exist_ok=True)
        self.filepath = os.path.join(self.config['base_directory'], filename)

    def listdir(self):
        return os.listdir(self.config['base_directory'])

    def is_bytes(self):
        try:
            with open(self.filepath, 'r') as file:
                file.read()
                return False
        except UnicodeDecodeError:
            return True

    def create(self):
        try:
            with open(self.filepath, 'w') as file:
                file.write('')
                return True
        except Exception:
            return False

    def update(self, content, is_bytes=False):
        try:
            with open(self.filepath, 'wb' if is_bytes else 'w') as file:
                file.write(content)
                return True
        except Exception:
            return False

    def read(self):
        with open(self.filepath, 'rb' if self.is_bytes() else 'r') as file:
            return file.read()

    def delete(self):
        try:
            os.remove(self.filepath)
            return True
        except Exception:
            return False


if __name__ == '__main__':
    g1 = File('../client_data/data/gambar.png')
    a = base64.encodebytes(g1.read()).decode('ascii')
    # print(json.dumps({'a': base64.encodebytes(g1.read()).decode('ascii')}))
    print(base64.decodebytes(a.encode()) == g1.read())
    print(g1.listdir())

    # g2 = File('new.png')
    # g2.update(g1.read(), True)

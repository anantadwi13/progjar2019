import os.path
from datetime import datetime
from glob import glob


class HttpServer:
    def __init__(self):
        self.sessions = {}
        self.types = {}
        self.types['.pdf'] = 'application/pdf'
        self.types['.jpg'] = 'image/jpeg'
        self.types['.txt'] = 'text/plain'
        self.types['.html'] = 'text/html'

    def response(self, kode=404, message='Not Found', messagebody='', headers={}):
        tanggal = datetime.now().strftime('%c')
        resp = []
        resp.append("HTTP/1.0 {} {}\r\n".format(kode, message))
        resp.append("Date: {}\r\n".format(tanggal))
        resp.append("Connection: close\r\n")
        resp.append("Server: myserver/1.0\r\n")
        resp.append("Content-Length: {}\r\n".format(len(messagebody)))
        for kk in headers:
            resp.append("{}:{}\r\n".format(kk, headers[kk]))
        resp.append("\r\n")
        resp.append("{}".format(messagebody))
        response_str = ''
        for i in resp:
            response_str = "{}{}".format(response_str, i)
        return response_str

    def proses(self, data):

        message = data.split("\r\n\r\n")

        headers = message[0].split("\r\n")
        content = message[1] if len(message) > 1 else ""

        baris = headers[0]

        all_headers = {n.split(": ", 1)[0]: n.split(": ", 1)[1] for n in headers[1:] if n != ''}

        j = baris.split(" ")
        try:
            method = j[0].upper().strip()
            if method == 'GET':
                object_address = j[1].strip()
                return self.http_get(object_address, all_headers)
            if method == 'POST':
                object_address = j[1].strip()
                return self.http_post(object_address, all_headers, content)
            else:
                return self.response(400, 'Bad Request', '', {})
        except IndexError:
            return self.response(400, 'Bad Request', '', {})

    def http_get(self, object_address, headers):
        files = glob('./*')
        thedir = '.'
        if thedir + object_address not in files:
            return self.response(404, 'Not Found', '', {})
        fp = open(thedir + object_address, 'r')
        isi = fp.read()

        fext = os.path.splitext(thedir + object_address)[1]
        content_type = self.types[fext]

        headers = {}
        headers['Content-type'] = content_type

        return self.response(200, 'OK', isi, headers)

    def http_post(self, object_address, headers, content):
        isi = ""

        isi += "===HEADER===\n"
        for header in headers.items():
            isi += "{:<30}: {}\n".format(header[0], header[1])

        isi += "\n===BODY===\n"
        for cont in content.split("&"):
            isi += "{}\n".format(cont)

        response_headers = {}
        return self.response(200, 'OK', isi, response_headers)


# >>> import os.path
# >>> ext = os.path.splitext('/ak/52.png')

if __name__ == "__main__":
    httpserver = HttpServer()
    d = httpserver.proses('GET testing.txt HTTP/1.0')
    print(d)
    d = httpserver.http_get('testing2.txt')
    print(d)
    d = httpserver.http_get('testing.txt')
    print(d)

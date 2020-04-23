class Request(object):
    def __init__(self):
        self.REQUEST_LINE: str or None = None
        self.HEADER: str or None = None
        self.HEADER_DICT: dict or None = None
        self.BODY: str or None = None

    def __str__(self):
        return "\nREQUEST_LINE:\n{}\n\nREQUEST_HEADER:\n{}\n\nREQUEST_BODY:\n{}".format(self.REQUEST_LINE, self.HEADER,
                                                                                        self.BODY)

    @staticmethod
    def load(data: str):
        req = Request()
        request = data.split("\r\n\r\n")
        temp = request[0].split("\r\n", 1)

        req.REQUEST_LINE = temp[0]
        req.HEADER = temp[1] if len(temp) > 1 else None
        req.BODY = request[1] if len(request) > 1 else None

        try:
            req.HEADER_DICT = {n.split(": ", 1)[0]: n.split(": ", 1)[1] for n in req.HEADER.split("\r\n") if n != ''}
        except:
            req.HEADER_DICT = None

        return req


class Response(object):
    def __init__(self):
        self.STATUS_LINE: str or None = None
        self.HEADER: str or None = None
        self.BODY: str or None = None

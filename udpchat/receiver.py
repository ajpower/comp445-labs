"""Receiver module for the UDP chat.

This handles accepting incoming connections and extracting the data from them.
"""
import socket
from udpmessage import Message

_CRLF = '\r\n'.encode('UTF-8')
_LF = '\n'.encode('UTF-8')


def _recvline(sock: socket.socket):
    """Receive a single line from the socket until EOF, close, or CRLF and
    return as a byte string.
    """
    BUFFER_SIZE = 1

    data = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE)
        if not last_buff:
            break
        data += last_buff
        if data.endswith(_CRLF):
            break
    return data


def _recv_preamble(conn: socket.socket):
    """Receives all the headers from the socket and return a RequestPreamble.
    """
    data = b''
    while True:
        last_line = _recvline(conn)
        if last_line == _CRLF or last_line == _LF:
            break
        else:
            data += last_line
    return RequestPreamble(data.decode('UTF-8'))


def _recvall(sock: socket.socket, length: int):
    """Receive all data from the socket until length, EOF, or close and return
    as a byte string.
    """
    BUFFER_SIZE = 8192

    data = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE)
        data += last_buff
        if not last_buff or len(data) >= length:
            break
    return data


def _extractData(sock: socket.socket):
    """Extracts the request data from the connection socket."""
    requestPreamble = _recv_preamble(sock)
    requestData = b''

    if 'Content-Length' in requestPreamble.headers:
        dataLength = int(requestPreamble.headers['Content-Length'])
        requestData = _recvall(sock, dataLength)

    return requestData


def receiver(port: int):
    """Start the receiver loop to accept incoming connections and extract their
    message.
    
    :param port: Source port.
    """
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.bind(('', port))
    sock.listen()

    while True:
        conn, _ = sock.accept()
        requestData = _extractData(conn)
        message = Message.parse(requestData)
        print(message)


class RequestPreamble:
    """Represents the HTTP request line and headers

    Attributes:
        http_method (str): HTTP Method.
        http_version (str): HTTP Version.
        url (str): Request URL
        headers (dict): Collection of key value pairs representing the request headers.
    """

    def __init__(self, preamble: str):
        """Parse the request preamble string."""
        # The first consecutive CRLF sequence demarcates the start of the
        # entity-body.
        preamble = preamble.strip()
        request_line, *headers = preamble.split("\r\n")
        self.http_method, self.url, self.http_version = request_line.split()
        headers = [self._remove_whitespace(s) for s in headers]
        self.headers = dict(kv.split(":", maxsplit=1) for kv in headers)

    @staticmethod
    def _remove_whitespace(s: str):
        """Return a string with all whitespace removed from the input."""
        return "".join(s.split())


class Request:
    """Represents an HTTP request.

    Attributes:
        preamble (RequestPreamble): Request preamble with request line and headers
        body (str): The request body.
    """

    def __init__(self, preamble: RequestPreamble, body: str):
        self.preamble = preamble
        self.body = body

    def __str__(self):
        """Return a string representation of the request."""
        request_line = "{} {} {}".format(self.preamble.http_method,
                                         self.preamble.url,
                                         self.preamble.http_version)
        headers = "\n".join(
            "{}: {}".format(k, v) for k, v in self.preamble.headers.items())
        return "\n".join((request_line, headers, self.body))

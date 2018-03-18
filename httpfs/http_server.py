"""Implements the socket listener and parsing of input"""

import socket
import logger
from threading import Thread
from abc import ABC, abstractmethod

http_server_version = 'HTTP/1.0'
http_server_CRLF = '\r\n'.encode('UTF-8')
http_server_CR = '\r'.encode('UTF-8')
http_server_LF = '\n'.encode('UTF-8')


def _has_new_line(data):
    return http_server_CRLF in data or http_server_CR in data or http_server_LF in data


def _recvline(sock: socket.socket):
    """Receive a single line from the socket until EOF, close or CRLF and return as a byte
    string.
    """
    BUFFER_SIZE = 1024

    data = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE)
        if not last_buff:
            break
        data += last_buff
        if _has_new_line(last_buff):
            break
    return data


def _recvall(sock: socket.socket, length: int):
    """Receive all data from the socket until length, EOF or close and return as a byte
    string.
    """
    BUFFER_SIZE = 8192

    data = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE)
        data += last_buff
        if not last_buff or len(data) >= length:
            break
    return data


def start_server(host, port: int, HTTPHandlerImplClass):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        logger.write('HTTP server listening at {}'.format(port))
        while True:
            conn, addr = listener.accept()
            handler_thread = ConnectionHandlerThread(conn, addr, HTTPHandlerImplClass)
            handler_thread.setDaemon(True)
            handler_thread.start()
    finally:
        listener.close()


class ConnectionHandlerThread(Thread):
    def __init__(self, conn, addr, HTTPHandlerImplClass):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.HTTPHandlerImplClass = HTTPHandlerImplClass

    def run(self):
        logger.write('Connection accepted from {}'.format(self.addr))
        try:
            server = HTTPServer(self.conn)
            request_preamble = self._recv_preamble()
            request_data = b''
            if 'Content-Length' in request_preamble.headers:
                data_length = request_preamble.headers['Content-Length']
                request_data = _recvall(self.conn, int(data_length))

            request = Request(request_preamble, request_data.decode('UTF-8'))

            http_handler = self.HTTPHandlerImplClass(request, server)
            http_handler.handle()
        except Exception as inst:
            logger(inst)
            server.error(500, 'Internal Server Error')
        finally:
            self.conn.close()

    def _recv_preamble(self):
        """Receives all the headers from the socket and return a RequestPreamble.
        """
        data = b''
        while True:
            last_line = _recvline(self.conn)
            if http_server_CRLF == last_line or http_server_LF == last_line:
                break
            else :
                data += last_line
        return RequestPreamble(data.decode('UTF-8'))


class HTTPServer:
    def __init__(self, conn):
        self.conn = conn

    def error(self, status: int, msg: str):
        response = "{} {} {}".format(http_server_version, status, msg)
        self.conn.sendall(response.encode("UTF-8"))
        self.conn.close()

    def response(self, status: int, data):
        ## TODO method stub and signature change
        pass


class HTTPHandler(ABC):
    def __init__(self, request: 'Request'   , server: HTTPServer):
        self.request = request
        self.server = server

    def handle(self):
        logger.write('handling request\n{}'.format(self.request))

        if self.request.preamble.http_method.casefold() == 'get'.casefold():
            self.do_GET()
        elif self.request.preamble.http_method.casefold() == 'post'.casefold():
            self.do_POST()
        else:
            self.do_invalid_method()

    @abstractmethod
    def do_GET(self):
        pass

    @abstractmethod
    def do_POST(self):
        pass

    @abstractmethod
    def do_invalid_method(self):
        pass


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
        map(self._remove_whitespace, headers)
        self.headers = dict(kv.split(":", maxsplit=1) for kv in headers)

    @staticmethod
    def _remove_whitespace(s: str):
        """Return a string with all whitespace removed from the input."""
        return "".join(s.split())


class Request:
    """Represents an HTTP request.

    Attributes:
        preamble (str): Request preamble with request line and headers
        body (str): The request body.
    """

    def __init__(self, preamble: RequestPreamble, body: str):
        """Parse the response string."""
        # The first consecutive CRLF sequence demarcates the start of the
        # entity-body.
        self.preamble = preamble
        self.body = body

    def __str__(self):
        """Return a string representation of the response."""
        request_line = "{} {} {}".format(self.preamble.http_method, self.preamble.url,
                                         self.preamble.http_version)
        headers = "\n".join(
            "{}: {}".format(k, v) for k, v in self.preamble.headers.items())
        return "\n".join((request_line, headers, self.body))

"""Implements functions for performing GET and POST requests."""
import socket
from urllib.parse import urlsplit


def _recvall(socket: socket.socket):
    """"""
    BUF_SIZE = 4096
    block = socket.recv(BUF_SIZE)
    data = block
    while len(block) == BUF_SIZE:
        block = socket.recv(BUF_SIZE)
        data += block
    return data


def _get_body(message: str):
    """"""
    # The first consecutive CRLF sequence demarcates the start of the
    # entity-body.
    i = message.find('\r\n\r\n')
    return '' if i == -1 else message[i+4:]


def GET(urlstr: str, headers=None, timeout=None, verbose=False):
    """TODO docstring.
    TODO handle timeout exception.
    """
    if not headers:
        headers = {}

    # Extract components from URL. If port is not specified default to 80.
    url = urlsplit(urlstr)
    netloc = url.netloc
    host = url.hostname
    port = url.port if url.port else 80
    path = url.path if url.path else '\\'
    query = url.query
    request_uri = '{}?{}'.format(path, query) if query else path

    # HTTP 1.1 requires Host header.
    headers.setdefault('Host', netloc)

    # Open a socket and connect to host, setting a timeout if necessary.
    socket_address = (host, port)
    sock = socket.socket(family=socket.AF_INET)
    if timeout:
        sock.settimeout(timeout)
    sock.connect(socket_address)

    # Construct HTTP request message.
    request_line = 'GET {} HTTP/1.0'.format(request_uri)
    headers_line = ''.join('{}:{}\r\n'.format(k, v)
                           for k, v in headers.items())
    entity_body = ''
    request = '\r\n'.join((request_line, headers_line, entity_body))

    # Send request message to host and retrieve the response message.
    sock.sendall(request.encode())
    response = _recvall(sock).decode('UTF-8')

    return response if verbose else _get_body(response)

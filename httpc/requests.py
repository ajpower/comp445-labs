"""Implements GET and POST request methods."""
import socket
from urllib.parse import urlparse


class Response:
    """Represents an HTTP response message.
    
    Attributes:
        http_version (str): HTTP version.
        code (int): Status code.
        status (str): Description of status code.
        headers (dict): Collection of key value pairs representing the response
            headers.
        body (str): The response body.
    """

    def __init__(self, response: str):
        """Parse the response string."""
        # The first consecutive CRLF sequence demarcates the start of the
        # entity-body.
        preamble, self.body = response.split("\r\n\r\n", maxsplit=1)
        status_line, *headers = preamble.split("\r\n")
        self.http_version, code, *status = status_line.split()
        self.code = int(code)
        self.status = " ".join(status)
        map(_remove_whitespace, headers)
        self.headers = dict(kv.split(":", maxsplit=1) for kv in headers)

    def __str__(self):
        """Return a string representation of the response."""
        status_line = "{} {} {}".format(self.http_version, self.code,
                                        self.status)
        headers = "\n".join(
            "{}: {}".format(k, v) for k, v in self.headers.items())
        return "\n".join((status_line, headers, self.body))


def _remove_whitespace(s: str):
    """Return a string with all whitespace removed from the input."""
    return "".join(s.split())


def _recvall(sock: socket.socket):
    """Receive all data from the socket until EOF or close and return as a byte
    string.
    """
    BUFFER_SIZE = 8192
    response = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE, socket.MSG_WAITALL)
        response += last_buff
        if len(last_buff) < BUFFER_SIZE:
            break

    return response


def GET(url: str, headers=None):
    """Perform an HTTP GET request. Return response as a Response object.

    Args:
        url (str): The URL to perform the GET request on.
        headers (dict): Dictionary containing key-value pairs representing the
            request headers. Default is None.

    Return:
        Response: The response from the host.
    """
    if not headers:
        headers = {}

    # Extract components from URL. If port is not specified default to 80.
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    host = parsed_url.hostname
    port = parsed_url.port or 80
    path = parsed_url.path or "\\"
    query = parsed_url.query
    request_uri = "{}?{}".format(path, query) if query else path

    # Add standard headers.
    headers.setdefault("Host", netloc)
    headers.setdefault("User-Agent", "Concordia-HTTP/1.0")

    # Construct HTTP request message.
    request_line = "GET {} HTTP/1.0".format(request_uri)
    headers_line = "".join(
        "{}:{}\r\n".format(k, v) for k, v in headers.items())
    entity_body = ""
    request = "\r\n".join((request_line, headers_line, entity_body))

    # Open a socket, connect to host, send request, and retrieve response.
    sock = socket.create_connection((host, port))
    sock.sendall(request.encode("UTF-8"))
    response = _recvall(sock).decode("UTF-8")

    return Response(response)


def POST(url: str, data="", headers=None):
    """Perform an HTTP POST request. Return response as a Response object.

    Args:
        url (str): The URL to perform the GET request on.
        data (str): Data to sent in request body. Defaults to empty string.
        headers (dict): Dictionary containing key-value pairs representing the
            request headers. Default is None.

    Returns:
        Response: The response from the host.
    """
    if not headers:
        headers = {}

    # Extract components from URL. If port is not specified default to 80.
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    host = parsed_url.hostname
    port = parsed_url.port or 80
    path = parsed_url.path or "\\"
    query = parsed_url.query
    request_uri = "{}?{}".format(path, query) if query else path

    # Add standard headers.
    headers.setdefault("Host", netloc)
    headers.setdefault("User-Agent", "Concordia-HTTP/1.0")
    headers.setdefault("Content-Length", str(len(data)))

    # Construct HTTP request message.
    request_line = "POST {} HTTP/1.0".format(request_uri)
    headers_line = "".join(
        "{}:{}\r\n".format(k, v) for k, v in headers.items())
    request = "\r\n".join((request_line, headers_line, data))

    # Open a socket, connect to host, send request, and retrieve response.
    sock = socket.create_connection((host, port))
    sock.sendall(request.encode("UTF-8"))
    response = _recvall(sock).decode("UTF-8")

    return Response(response)

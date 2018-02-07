"""Implements functions for performing GET and POST requests."""
import socket
from urllib.parse import urlsplit
from urllib.parse import urlparse

# Receives all the data from the socket until EOF or close.
def _recvall(socket: socket.socket):
    """"""
    BUFFER_SIZE = 8192
    response = b""
    while True:
        last_buff = sock.recv(BUFFER_SIZE, socket.MSG_WAITALL)
        response += last_buff
        if len(last_buff) < BUFFER_SIZE:
            break

    return response


def _get_body(message: str):
    """"""
    # The first consecutive CRLF sequence demarcates the start of the
    # entity-body.
    i = message.find('\r\n\r\n')
    return '' if i == -1 else message[i+4:]


def GET(urlstr: str, headers=None, timeout=None, verbose=False):
    """TODO docstring.
    TODO handle timeout exception.
    TODO check url format?
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


# Send a post request to the given url, with the data and headers.
# Prints debug information if verbose is set TODO verbose flag
#
# The function returns a dictionary with the key headers, body and status
def POST(url: str, data=None, headers={}, verbose=False):
    parsed_url = urlparse(url)
    port = parsed_url.port if parsed_url.port else 80
    method = "POST"
    http_version = "1.0"

    content_length = len(data) if data else 0

    # Add Standard headers
    headers["Host"] = parsed_url.hostname
    headers["User-Agent"] = "Concordia-HTTP/1.0"
    headers["Content-Length"] = str(content_length)

    header_txt = build_headers(headers)

    # Build request
    request = method + " " + parsed_url.path + " HTTP/" + http_version + "\r\n"
    request += header_txt
    request += "\r\n"

    if data is not None:
        request += data

    # Call server
    sock = socket.create_connection((parsed_url.hostname, port))
    sock.sendall(request.encode("utf-8"))
    response = _recvall(sock).decode("utf-8")

    response = parse_response(response)
    return response


# Parse the response string and returns a dict with headers, body, status{code,text}
def parse_response(response: str):
    response = response.split("\r\n\r\n")
    headers = response[0].split("\r\n")
    body = response[1]

    status = headers[0].split(" ")
    status_code = int(status[1])
    status_txt = status[2]

    headers = parse_headers(headers[1:])
    return {"status": {"code" : status_code, "text": status_txt}, "headers": headers, "body": body}


# Parse a list of headers line into a dict of name : value
def parse_headers(headers):
    header_map = {}
    for header in headers:
        prs = header.split(":")
        name = prs[0].strip()
        val = prs[1].strip()
        header_map[name] = val

    return header_map


# Builds a string of headers from a dict of name : val
def build_headers(headers):
    header_text = ""
    for name, val in headers.items():
        header_text += name + " : " + val + "\r\n"
    return header_text


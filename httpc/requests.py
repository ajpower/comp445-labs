"""Implements functions for performing GET and POST requests."""
import socket
from urllib.parse import urlsplit
from urllib.parse import urlparse


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
def post(url: str, data=None, headers={}, verbose=False):
    parsedurl = urlparse(url)
    port = parsedurl.port
    method = "POST"
    httpversion = "1.0"
    if port is None:
        port = 80

    if data is None:
        contentlength = 0
    else:
        contentlength = len(data)

    # Add Standard headers
    headers["Host"] = parsedurl.hostname
    headers["User-Agent"] = "Concordia-HTTP/1.0"
    headers["Content-Length"] = str(contentlength)

    headertxt = buildheaders(headers)

    # Build request
    request = method + " " + parsedurl.path + " HTTP/" + httpversion + "\r\n"
    request += headertxt
    request += "\r\n"

    if data is not None:
        request += data

    # Call server
    sock = socket.create_connection((parsedurl.hostname, port))
    sock.sendall(request.encode("utf-8"))
    response = recvall(sock).decode("utf-8")

    response = parseresponse(response)
    return response

# Parse the response string and returns a dict with headers, body, status{code,text}
def parseresponse(response: str):
    response = response.split("\r\n\r\n")
    headers = response[0].split("\r\n")
    body = response[1]

    status = headers[0].split(" ")
    statuscode = int(status[1])
    statustxt = status[2]

    headers = parseheaders(headers[1:])
    return {"status": {"code" : statuscode, "text": statustxt}, "headers": headers, "body": body}

# Parse a list of headers line into a dict of name : value
def parseheaders(headers):
    headermap = {}
    for header in headers:
        prs = header.split(":")
        name = prs[0].strip()
        val = prs[1].strip()
        headermap[name] = val

    return headermap

# Builds a string of headers from a dict of name : val
def buildheaders(headers):
    headertext = ""
    for name, val in headers.items():
        headertext += name + " : " + val + "\r\n"
    return headertext

# Receives all the data from the socket until EOF or close.
def recvall(sock):
    BUFFER_SIZE = 8192
    response = b""
    while True:
        lastbuff = sock.recv(BUFFER_SIZE, socket.MSG_WAITALL)
        response += lastbuff
        if len(lastbuff) < BUFFER_SIZE:
            break

    return response

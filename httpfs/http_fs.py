import logger
import http_server
from file_manager import set_dir, list_dir, get_file, write_file
from http_server import HTTPHandler


def start_file_server(host, port: int, directory: str = '.'):
    """Start the HTTP file server with host and listening on port This will use http_server module.
    Uses the HTTPHandlerFs as the HTTPHandler
    :param host: hostname of the server.
    :param port: port to listen for new connection.
    :param directory: (str) Directory for the file server. Defaults to current directory.
    """
    set_dir(directory)
    http_server.start_server(host, port, HTTPHandlerFs)


class HTTPHandlerFs(HTTPHandler):
    def do_GET(self):
        logger.write('It works GET\n{}'.format(self.request))
        self.server.send_response('This is a response\r\n')

    def do_POST(self):
        logger.write('It works POST\n{}'.format(self.request))

    def do_invalid_method(self):
        logger.write('It works invalid\n{}'.format(self.request))

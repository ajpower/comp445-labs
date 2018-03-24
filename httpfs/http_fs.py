import logger
import http_server
import json
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
        logger.write('Handler GET requestURL: {}'.format(self.request.preamble.url))

        url = self.request.preamble.url
        if url == "/":
            files = json.dumps({'files': list_dir()})
            self.server.send_response(files, {"Content-Type": "application/json"})
        elif not url.startswith("/"):
            self.server.send_error("400", "Bad Request")
        else:
            try:
                self.server.send_response(get_file(url.lstrip("/")), {"Content-Type": "text/*"})
            except Exception as err:
                logger.write(err)
                self.server.send_error("404", "Not Found")

    def do_POST(self):
        logger.write('Handler POST requestURL: {}'.format(self.request.preamble.url))

        url = self.request.preamble.url
        if not url.startswith("/"):
            self.server.send_error("400", "Bad Request")
        else:
            try:
                write_file(url.lstrip("/"), self.request.body)
                self.server.send_response()
            except Exception as err:
                logger.write(err)
                self.server.send_error("400", "Bad Request")
            logger.write('File correctly added')

    def do_invalid_method(self):
        logger.write('Invalid Method \n{}'.format(self.request))

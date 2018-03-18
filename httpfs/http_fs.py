import logger
from http_server import HTTPHandler


class HTTPHandlerFs(HTTPHandler):
    def do_GET(self):
        logger.write('It works GET\n{}'.format(self.request))

    def do_POST(self):
        logger.write('It works POST\n{}'.format(self.request))

    def do_invalid_method(self):
        logger.write('It works invalid\n{}'.format(self.request))

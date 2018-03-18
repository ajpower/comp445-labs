import logger
import http_server
from http_fs import HTTPHandlerFs


logger.set_logger(True)
http_server.start_server('127.0.0.1', 8080, HTTPHandlerFs)

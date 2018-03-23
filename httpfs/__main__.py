import logger
import http_fs


logger.set_logger(True)
http_fs.start_file_server('127.0.0.1', 8080)

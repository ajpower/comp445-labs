import argparse
import logger
import http_fs

DEFAULT_PORT = 8080

parser = argparse.ArgumentParser(description='httpfs is a simple file server.')
parser.add_argument(
    '-v',
    dest='verbose',
    action='store_true',
    help='Prints debugging messages.')
parser.add_argument(
    '-p',
    dest='port',
    type=int,
    help=(
        'Specifies the port number that the server will listen and serve at. '
        'Default is {}.'.format(DEFAULT_PORT)),
    default=DEFAULT_PORT,
    metavar='PORT')
parser.add_argument(
    '-d',
    dest='dir',
    help=
    ('Specifies the directory that the server will use to read/write requested '
     'files. Default is the current directory when launching the application.'
     ),
    default='.',
    metavar='PATH-TO-DIR')

args = parser.parse_args()

logger.set_logger(args.verbose)
http_fs.start_file_server('127.0.0.1', port=args.port, directory=args.dir)

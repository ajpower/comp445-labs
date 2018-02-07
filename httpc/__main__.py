"""Executes the httpc program."""
import argparse
from requests import GET
from requests import POST

def execute_help(args):
    """"""


def execute_get(args):
    """"""
    headers = dict(kv.split(':') for kv in args.headers)
    response = GET(args.url, headers=headers, verbose=args.verbose)
    print(response)


def execute_post(args):


parser = argparse.ArgumentParser(
    description='httpc is a curl-like application but supports HTTP protocol only.', add_help=False)
subparsers = parser.add_subparsers(
    title='command', metavar='command')

get_parser = subparsers.add_parser(
    'get', description='Get executes a HTTP GET request for a given URL.', add_help=False)
get_parser.add_argument(
    '-v', help='Prints the detail of the response such as protocol, status, and headers.',
    action='store_true', dest='verbose')
get_parser.add_argument(
    '-h', help="Associates headers to HTTP Request with the format 'key:value'.",
    metavar='key:value', action='append', default=[], dest='headers')
get_parser.add_argument('url', metavar='URL')
get_parser.set_defaults(func=execute_get)

post_parser = subparsers.add_parser('post', description='Post executes a HTTP POST request for a given URL and body.',
                                    add_help=False)
post_parser.add_argument('-v', help='Prints the detail of the response such as protocol, status, and headers.',
                         action='store_true', dest='verbose')
post_parser.add_argument('-h', help="Associates headers to HTTP Request with the format 'key:value'.",
                         metavar='key:value', action='append', default=[], dest='headers')
post_parser.add_argument('-d', help='Associates an inline data to the body HTTP POST request')
post_parser.add_argument('-f', help='ssociates the content of a file to the body HTTP POST request.')
post_parser.add_argument('url', metavar='URL')
post_parse.set_defaults(func=execute_post)

help_parser = subparsers.add_parser('help', add_help=False)
help_parser.add_argument('command', choices=(
    'get', 'put'), nargs='?', metavar='command')
# help_parser.set_defaults(func=execute_help)

args = parser.parse_args()

try:
    args.func(args)
except AttributeError:
    parser.print_help()

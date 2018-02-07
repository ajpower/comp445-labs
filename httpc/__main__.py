"""Executes the httpc program."""
import argparse
from requests import GET


def execute_help(args):
    """"""
    print('TODO')


def execute_get(args):
    """"""
    headers = {k: v for k, v in map(lambda h: h.split(':'), args.headers)}
    response = GET(args.url, headers=headers, verbose=args.verbose)
    print(response)


parser = argparse.ArgumentParser(
    description='httpc is a curl-like application but supports HTTP protocol only.', add_help=False)
subparsers = parser.add_subparsers(title='commaInd')

get_parser = subparsers.add_parser(
    'get', description='Get executes a HTTP GET request for a given URL.', add_help=False)
get_parser.add_argument(
    '-v', help='Prints the detail of the response such as protocol, status, and headers.',
    action='store_true', dest='verbose')
get_parser.add_argument(
    '-h', help="Associates headers to HTTP Request with the format 'key:value'.",
    metavar='key:value', action='append', dest='headers')
get_parser.add_argument('url', metavar='URL')
get_parser.set_defaults(func=execute_get)

help_parser = subparsers.add_parser('help', add_help=False)
help_parser.add_argument('command', choices=(
    'get', 'put'), nargs='?', metavar='command')
help_parser.set_defaults(func=execute_help)

args = parser.parse_args()
args.func(args)

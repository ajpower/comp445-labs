"""Executes the httpc program."""
import argparse
from requests import GET, POST


def execute_get(args):
    """"""
    headers = dict(kv.split(':') for kv in args.headers)
    response = GET(args.url, headers=headers)
    print(response if args.verbose else response.body)


def execute_post(args):
    """"""
    # Extract data depending on whether inline-data or file was specified.
    if args.file:
        with open(args.file, mode='r') as f:
            data = f.read()
    else:
        data = args.inline_data

    headers = dict(kv.split(':') for kv in args.headers)
    response = POST(args.url, data=data, headers=headers)
    print(response if args.verbose else response.body)


parser = argparse.ArgumentParser(
    description=
    'httpc is a curl-like application but supports HTTP protocol only.',
    add_help=False)
subparsers = parser.add_subparsers(title='command', metavar='command')

get_parser = subparsers.add_parser(
    'get',
    description='Get executes a HTTP GET request for a given URL.',
    add_help=False)
get_parser.add_argument(
    '-v',
    help=
    'Prints the detail of the response such as protocol, status, and headers.',
    action='store_true',
    dest='verbose')
get_parser.add_argument(
    '-h',
    help="Associates headers to HTTP Request with the format 'key:value'.",
    metavar='key:value',
    action='append',
    default=[],
    dest='headers')
get_parser.add_argument('url', metavar='URL')
get_parser.set_defaults(func=execute_get)

post_parser = subparsers.add_parser(
    'post',
    description='Post executes a HTTP POST request for a given URL and body.',
    add_help=False)
post_parser.add_argument(
    '-v',
    help=
    'Prints the detail of the response such as protocol, status, and headers.',
    action='store_true',
    dest='verbose')
post_parser.add_argument(
    '-h',
    help="Associates headers to HTTP Request with the format 'key:value'.",
    metavar='key:value',
    action='append',
    default=[],
    dest='headers')
data_group = post_parser.add_mutually_exclusive_group(required=True)
data_group.add_argument(
    '-d',
    help='Associates an inline data to the body HTTP POST request',
    metavar='inline-data',
    dest='inline_data')
data_group.add_argument(
    '-f',
    help='Associates the content of a file to the body HTTP POST request.',
    metavar='file',
    dest='file')
post_parser.add_argument('url', metavar='URL')
post_parser.set_defaults(func=execute_post)

help_parser = subparsers.add_parser('help', add_help=False)
help_parser.add_argument(
    'command', choices=('get', 'put'), nargs='?', metavar='command')
# help_parser.set_defaults(func=execute_help)

args = parser.parse_args()

args.func(args)

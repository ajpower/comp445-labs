"""Executes the httpc program."""
import argparse
from requests import GET, POST


def execute_get(args):
    """Perform a GET request with the given command line parameters and print
    the responset to standard out.

    Args:
        args: Argparse argument object.
    """
    headers = dict(kv.split(":") for kv in args.headers)
    url = args.url
    while True:
        response = GET(url, headers=headers)
        print(response if args.verbose else response.body)
        if response.code == 301 or response.code == 302:
            url = response.headers['Location'].strip()
            print('Redirecting to new url: {}'.format(url))
        else:
            break



def execute_post(args):
    """Perform a PUT request with the given command line parameters and print
    the responset to standard out.

    Args:
        args: Argparse argument object.
    """
    # Extract data, either by reading a file or using the inline data.
    # TODO check if file exists.
    if args.file:
        with open(args.file, mode="r") as f:
            data = f.read()
    else:
        data = args.inline_data

    headers = dict(kv.split(":") for kv in args.headers)
    url = args.url
    while True:
        response = POST(url, data=data, headers=headers)
        print(response if args.verbose else response.body)
        if response.code == 301 or response.code == 302:
            url = response.headers['Location'].strip()
            print('Redirecting to new url: {}'.format(url))
        else:
            break


parser = argparse.ArgumentParser(
    description=
    "httpc is a curl-like application but supports HTTP protocol only.",
    add_help=False,
    epilog='Use "httpc help [command]" for more information about a command.')
subparsers = parser.add_subparsers(
    title="The commands are",
    help="""
get executes a HTTP GET request and prints the response.
post executes a HTTP POST request and prints the response.
help prints this screen.""")

get_parser = subparsers.add_parser(
    "get",
    description="Get executes a HTTP GET request for a given URL.",
    add_help=False)
get_parser.add_argument(
    "-v",
    help=
    "Prints the detail of the response such as protocol, status, and headers.",
    action="store_true",
    dest="verbose")
get_parser.add_argument(
    "-h",
    help="Associates headers to HTTP Request with the format 'key:value'.",
    metavar="key:value",
    action="append",
    default=[],
    dest="headers")
get_parser.add_argument("url", help="The URL of the host.", metavar="URL")
get_parser.set_defaults(func=execute_get)

post_parser = subparsers.add_parser(
    "post",
    description="Post executes a HTTP POST request for a given URL and body.",
    add_help=False)
post_parser.add_argument(
    "-v",
    help=
    "Prints the detail of the response such as protocol, status, and headers.",
    action="store_true",
    dest="verbose")
post_parser.add_argument(
    "-h",
    help="Associates headers to HTTP Request with the format 'key:value'.",
    metavar="key:value",
    action="append",
    default=[],
    dest="headers")
data_group = post_parser.add_mutually_exclusive_group(required=True)
data_group.add_argument(
    "-d",
    help="Associates an inline data to the body HTTP POST request",
    metavar="inline-data",
    dest="inline_data")
data_group.add_argument(
    "-f",
    help="Associates the content of a file to the body HTTP POST request.",
    metavar="file",
    dest="file")
post_parser.add_argument("url", help="The URL of the host.", metavar="URL")
post_parser.set_defaults(func=execute_post)

help_parser = subparsers.add_parser("help", add_help=False)
help_parser.add_argument(
    "command", choices=("get", "post"), nargs="?", metavar="command")
parser.set_defaults(command=None)

args = parser.parse_args()
try:
    args.func(args)
except AttributeError:
    if args.command is None:
        parser.print_help()
    elif args.command == "get":
        get_parser.print_help()
    elif args.command == "post":
        post_parser.print_help()

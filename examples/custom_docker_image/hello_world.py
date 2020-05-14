import logging
from argparse import ArgumentParser, Namespace

logger = logging.getLogger(__name__)


def parse_args(sub_parser: ArgumentParser):
    subparser = sub_parser.add_parser('hello_world', help='Logs hello message')
    subparser.set_defaults(func=hello_world)


def hello_world(args: Namespace):
    logger.success('hello from commands-base!')

#!/usr/bin/env python3

import argparse
import logging
import pkgutil
import os

import coloredlogs
import verboselogs


def main():
    verboselogs.install()
    project_name = os.environ.get("PROJECT_NAME")
    # Discover all the commands defined in derived image
    parser = argparse.ArgumentParser(description=f"Managing {project_name} commands")
    parser.add_argument(
        "--log-level",
        choices=sorted(logging._nameToLevel, key=lambda name: logging._nameToLevel[name]),
        default="INFO",
    )

    # Import our commands and ask them to populate the subparsers with their argument configurations
    gather_commands(
        subparsers=parser.add_subparsers(help="Sub-commands"),
        commands_directory=os.environ.get("ALADDIN_COMMANDS_PATH", "/code/commands"),
    )

    # Actually parse the arguments
    args = parser.parse_args()

    # Use the provided log level and upgrade our logging capabilities
    coloredlogs.install(
        level=logging._nameToLevel[args.log_level],
        fmt="%(levelname)-8s %(name)s(%(lineno)d) %(message)s",
        level_styles=dict(
            spam=dict(color="white", faint=True),
            debug=dict(color="black", bold=True),
            verbose=dict(color="blue"),
            info=dict(color="white"),
            notice=dict(color="magenta"),
            warning=dict(color="yellow"),
            success=dict(color="green", bold=True),
            error=dict(color="red"),
            critical=dict(color="red", bold=True),
        ),
        field_styles=dict(
            asctime=dict(color="green"),
            hostname=dict(color="magenta"),
            levelname=dict(color="white"),
            name=dict(color="white", bold=True),
            programname=dict(color="cyan"),
            username=dict(color="yellow"),
        ),
    )

    try:
        # Invoke the requested command
        args.func(args)
    except AttributeError:
        parser.print_help()


def gather_commands(subparsers: argparse.Action, commands_directory: str):
    """Search for available commands and gather their arguments."""
    for finder, command_name, _ in pkgutil.iter_modules([commands_directory]):
        loader = finder.find_module(command_name)
        command_module = loader.load_module()
        command_module.parse_args(subparsers)


if __name__ == "__main__":
    main()

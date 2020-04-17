#!/usr/bin/env python3

import argparse
import logging
import pathlib
import pkgutil
import os

import coloredlogs
import verboselogs


def main(project_name: str):
    # Discover all the commands defined in derived image
    parser = argparse.ArgumentParser(description=f"Managing {project_name} commands")
    parser.add_argument(
        "--log-level",
        choices=sorted(logging._nameToLevel, key=lambda name: logging._nameToLevel[name]),
        default="INFO",
    )

    # Import our commands and ask them to populate the subparsers with their argument configurations
    subparsers = parser.add_subparsers(help="Sub-commands")
    commands_directory = pathlib.Path("/code") / "commands"
    gather_commands(subparsers, commands_directory)

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
            info=dict(color="cyan"),
            notice=dict(color="magenta"),
            warning=dict(color="yellow"),
            success=dict(color="green", bold=True),
            error=dict(color="red"),
            critical=dict(color="red", bold=True),
        ),
    )

    # Invoke the requested command
    args.func(args)


def gather_commands(subparsers: argparse.Action, directory: pathlib.Path):
    """Search for available commands and gather their arguments."""
    for _, command_name, _ in pkgutil.iter_modules([directory]):
        commands_package = __import__(f"{directory.stem}.{command_name}")
        command_module = getattr(commands_package, command_name)
        command_module.parse_args(subparsers)


if __name__ == "__main__":
    logging.setLoggerClass(verboselogs.VerboseLogger)
    main(os.environ.get("PROJECT_NAME"))

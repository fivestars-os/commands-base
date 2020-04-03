import argparse
import logging
import os
import pkgutil


def main(project_name):
    # Discover all the commands defined in derived image
    parser = argparse.ArgumentParser(description=f"Managing {project_name} commands")
    parser.add_argument("--log-level", choices=logging._nameToLevel, default="INFO")

    subparsers = parser.add_subparsers(help="sub commands")
    gather_commands(subparsers, "commands")

    # Actually parse the arguments
    args = parser.parse_args()

    # Apply the log level to the basic config
    logging.basicConfig(
        format="%(levelname)-8s %(name)s(%(lineno)d) %(message)s",
        level=logging._nameToLevel[args.log_level],
    )

    # Invoke the requested command
    args.func(args)


def gather_commands(subparsers, directory):
    # Search for available commands and gather their arguments
    for _, command_name, _ in pkgutil.iter_modules([directory]):
        commands_package = __import__(f"{directory}.{command_name}")
        command_module = getattr(commands_package, command_name)
        command_module.parse_args(subparsers)


if __name__ == "__main__":
    main(os.environ.get("PROJECT_NAME"))

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="commands-base",
    version="2.0.0",
    author="Fivestars",
    author_email="dev@fivestars.com",
    description="Base command for aladdin commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fivestars-os/commands-base",
    packages=[
        "commands_base"
    ],
    entry_points={
        "console_scripts": [
            "aladdin_command = commands_base:main",
        ]
    },
)

FROM fivestarsos/commands-base:2.0.0

ENV PROJECT_NAME='commands-base-example'

# Poetry (https://python-poetry.org/) is already installed and available too
# So you can do the following:

# COPY pyproject.toml poetry.lock ./
# RUN poetry install

# commands are expected to be in `/code/commands`
# WORKDIR is already set to `/code`
COPY hello_world.py commands/hello_world.py


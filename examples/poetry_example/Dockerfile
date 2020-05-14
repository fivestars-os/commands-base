##  Could be any base image, only build dependencies are git and pip
FROM python:3.8-slim

ENV PROJECT_NAME='commands-base-example'
ARG POETRY_VERSION=1.0.5

ENV PATH="/root/.poetry/bin:${PATH}"

RUN apt-get install -y git && pip3 install --upgrade pip && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /the/workdir/path

COPY pyproject.toml ./
# In your project you should also copy your auto-generated lock file:
# COPY poetry.lock ./
COPY poetry.toml /root/.config/pypoetry/config.toml

COPY commands_base_example commands_base_example
ENV ALADDIN_COMMANDS_PATH='/the/workdir/path/commands_base_example'

RUN poetry install

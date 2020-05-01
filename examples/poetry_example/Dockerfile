##  Could be any base image, only build dependencies are git and pip
FROM python:3.8-slim

ENV PROJECT_NAME='commands-base-example'

RUN apt-get update && apt-get install -y git && \
    pip install poetry==1.0.5
WORKDIR /the/workdir/path
ENV ALADDIN_COMMANDS_PATH='/the/workdir/path/commands_base_example'

COPY pyproject.toml ./
COPY commands_base_example commands_base_example
COPY poetry.toml /root/.config/pypoetry/config.toml

RUN poetry install

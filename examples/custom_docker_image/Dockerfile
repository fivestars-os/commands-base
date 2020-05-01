##  Could be any base image, only build dependencies are git and pip
FROM python:3.8-slim

ENV PROJECT_NAME='commands-base-example'

RUN apt-get update && apt-get install -y git && \
    pip install git+https://github.com/fivestars-os/commands-base@2.0.1 && \
    apt-get clean
WORKDIR /the/workdir/path
ENV ALADDIN_COMMANDS_PATH='/the/workdir/path'

COPY hello_world.py .

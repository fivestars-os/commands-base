#! /usr/bin/env sh
set -eu

docker build -t "commands-base:${HASH:-local}" .

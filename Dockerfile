# Inherit from this docker image and copy your project's commands directory
# to the /code/commands folder and any other necessary files into
# the /code directory

FROM python:3.8-slim

WORKDIR /code

COPY command.py .

# Sleep infinity equivalent
ENTRYPOINT ["tail", "-f",  "/dev/null"]

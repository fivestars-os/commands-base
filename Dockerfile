########################################################################################
# Inherit from this docker image and copy your project's commands into the
# /code/commands directory. Any other supporting files can go in the /code
# directory. The /code directory will be added to PYTHONPATH.
########################################################################################


### BUILD POETRY PACKAGE MANAGER AND INSTALL DEPENDENCIES ##############################
# This downloads, installs and configures the poetry tool under the root user in the
# build image. It then installs the python package dependencies specified in the
# pyproject.toml file according to the frozen versions in poetry.lock.
########################################################################################
FROM python:3.8-slim as builder

# Install packages required to build native library components
RUN apt-get update \
 && apt-get -y --no-install-recommends install \
    gettext \
    gcc \
    g++ \
    make \
    libc6-dev \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Configure pip
COPY pip.conf /etc/pip.conf

# Install poetry
ARG POETRY_VERSION=1.0.5
ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /tmp/get-poetry.py
RUN python /tmp/get-poetry.py --version $POETRY_VERSION

# Configure poetry
COPY poetry.toml /root/.config/pypoetry/config.toml

# Install our python package and dependencies
WORKDIR /build
COPY pyproject.toml poetry.lock setup.py README.md ./
COPY commands_base commands_base
RUN . /root/.poetry/env \
 && poetry install \
 && pip install .
### END BUILDER IMAGE ##################################################################



### INSTALL POETRY PACKAGE MANAGER AND THE COMMAND.PY SCRIPT ###########################
# Copy the poetry tool and its configuration into the target image. This also includes
# a bit of pip global configuration since poetry uses it under the hood.
########################################################################################
FROM python:3.8-slim
LABEL maintainer="dev@fivestars.com"

# Configure pip
COPY --from=builder /etc/pip.conf /etc/pip.conf

# Copy installed python packages from build image
COPY --from=builder /root/.poetry /root/.poetry

# Configure poetry
COPY --from=builder /root/.config/pypoetry /root/.config/pypoetry

# Add poetry directories to PATH
ENV PATH /root/.local/bin:/root/.poetry/bin:$PATH

# Copy installed packages from build image
COPY --from=builder /root/.local /root/.local

# Create the /code directory for derived images to populate and add it to sys.path
WORKDIR /code
ENV PYTHONPATH=/code

# Sleep infinity equivalent
ENTRYPOINT ["tail", "-f",  "/dev/null"]
### END IMAGE BUILD ####################################################################

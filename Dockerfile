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
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install poetry
ARG POETRY_VERSION=1.7.1
ENV PATH /root/.local/bin:$PATH
RUN curl -sSL https://install.python-poetry.org -o install-poetry.py && \
    python install-poetry.py --version $POETRY_VERSION
ENV POETRY_VIRTUALENVS_CREATE="false"

ENV PATH /venv/bin:$PATH
ENV VIRTUAL_ENV=/venv

RUN python -m venv /venv && \
    pip install --upgrade pip

# Install our python package and dependencies
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --no-root
COPY commands_base commands_base
RUN poetry install
### END BUILDER IMAGE ##################################################################



### INSTALL POETRY PACKAGE MANAGER AND THE COMMAND.PY SCRIPT ###########################
# Copy the poetry tool and its configuration into the target image. This also includes
# a bit of pip global configuration since poetry uses it under the hood.
########################################################################################
FROM python:3.8-slim
LABEL maintainer="dev@fivestars.com"

# Add poetry directories to PATH
ENV PATH /root/.local/bin:/venv/bin:$PATH

# Copy installed python packages from build image
COPY --from=builder /root/.local /root/.local
# Copy installed packages from build image
COPY --from=builder /venv /venv

# Create the /code directory for derived images to populate and add it to sys.path
WORKDIR /code
ENV PYTHONPATH=/code

# Sleep infinity equivalent
ENTRYPOINT ["tail", "-f",  "/dev/null"]
### END IMAGE BUILD ####################################################################

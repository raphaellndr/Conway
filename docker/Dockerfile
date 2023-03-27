ARG PYTHON_VERSION="3.9"

FROM python:${PYTHON_VERSION}-slim as deps

ENV PIP_IGNORE_INSTALLED 1
ENV PYTHONUSERBASE /app
WORKDIR "$PYTHONUSERBASE"
WORKDIR /src

# Install dependencies
COPY pyproject.toml poetry.lock ./
# Add required files for dependencies installation to complete
RUN mkdir -p src/conway && touch README.md src/conway/__init__.py
# Install dependencies
RUN python3.9 -m pip install --user .
# Remove dummy files
RUN rm -rf src README.md
# Install application
COPY . ./
RUN python3.9 -m pip install --user .

################################################################################

FROM python:${PYTHON_VERSION}-slim

ENV PYTHONUSERBASE /app
WORKDIR "$PYTHONUSERBASE"

COPY --from=deps /app "$PYTHONUSERBASE"

RUN useradd -M conway
USER conway

ENTRYPOINT ["/app/bin/conway"]

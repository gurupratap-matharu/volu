# Build requirements.txt from poetry.lock
FROM python:3.10-slim as poetry
WORKDIR /code
RUN pip install poetry
COPY ./backend/pyproject.toml ./backend/poetry.lock /code/
RUN poetry export --output requirements.txt


# Pull base image
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work dir
WORKDIR /code

# copy requirements.txt from previous stage
COPY --from=poetry /code/requirements.txt /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY ./backend/ /code/

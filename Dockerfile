# Pull base image
FROM python:3-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work dir
WORKDIR /code

# install requirements
COPY ./backend/requirements.txt /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY ./backend/ /code/
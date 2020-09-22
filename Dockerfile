FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

COPY . /code/
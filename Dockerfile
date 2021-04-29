FROM python:3.8

# RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install pipenv
WORKDIR /code

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

COPY . .
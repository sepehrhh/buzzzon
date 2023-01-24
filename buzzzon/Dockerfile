FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get install -y netcat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

RUN ["chmod", "+x", "/usr/src/app/docker-entrypoint.sh"]

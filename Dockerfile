# pull official base image
FROM python:3.9.6-alpine

# create wrk directory
RUN mkdir /univast

# set work directory
WORKDIR /univast

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip

# copy requirements from codebase to work directory
COPY ./requirements.txt /requirements.txt

# do something I can't remember but don't delete.
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev

# install requirements
RUN pip install -r /requirements.txt

# delete something I can't remember but don't delete.
RUN apk del .tmp

# copy project
COPY . .
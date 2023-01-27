# pull official base image
FROM python:3.9.6-alpine

EXPOSE 8000

# create wrk directory
RUN mkdir /univast

# set work directory
WORKDIR /univast

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
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

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["sh", "-c", "0.0.0.0:8000", "Univast.wsgi"]
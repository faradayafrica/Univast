# pull official base image
FROM python:3.9-slim-buster

# create work directory
RUN mkdir /univast

# set work directory
WORKDIR /univast

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port 8000
EXPOSE 8000

# copy dependencies
COPY ./requirements.txt /requirements.txt

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# copy project
COPY . .
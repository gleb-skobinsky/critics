# base image
FROM python:3.11.9-alpine3.19
# setup environment variable
ENV DockerHOME=/home/app/webapp

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD ./requirements.txt $DockerHOME/requirements.txt

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . $DockerHOME
# run this command to install all dependencies
RUN pip install -r requirements.txt

ADD . $DockerHOME
# port where the Django app runs
EXPOSE 8000
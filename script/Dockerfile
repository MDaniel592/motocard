# pull official base image
FROM python:3.10.9-slim-buster

# Install the requirements packages
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN apt-get install apt-utils libpq-dev gcc -y

WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/
RUN python3 -m pip install -r requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# set work directory
COPY ./ /usr/src/app/

# start
CMD ["python3", "/usr/src/app/producer.py"]


FROM python:3.10.9-slim-buster

WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/
RUN python3 -m pip install -r requirements.txt

# set work directory
COPY ./consumer.py /usr/src/app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# start
CMD ["python3", "/usr/src/app/consumer.py"]


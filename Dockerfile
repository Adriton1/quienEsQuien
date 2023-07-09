FROM python:3.8.2-slim-buster

RUN apt-get update && apt-get -y install libpq-dev gcc


RUN mkdir /quienEsquien_App

WORKDIR /quienEsquien_App

COPY requirements.txt /quienEsquien_App/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /quienEsquien_App/



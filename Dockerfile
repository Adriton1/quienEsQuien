FROM python:3.9.13-alpine3.16

RUN apk update && apk upgrade \
    && apk add postgresql-client \
        postgresql-dev \
        musl-dev \
        gcc \
        linux-headers \
        gettext-dev \
    && pip install pipenv

RUN mkdir /quienEsquien_App

WORKDIR /quienEsquien_App

COPY requirements.txt /quienEsquien_App/

RUN pip install -r requirements.txt

COPY . /quienEsquien_App/


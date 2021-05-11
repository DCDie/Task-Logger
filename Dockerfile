FROM python:3.7

ENV PYTHONBUFFERED 1

WORKDIR /Milestone2

ADD . /Milestone2

COPY ./requirements.txt /Milestone2/requirements.txt

RUN pip install -r requirements.txt

COPY . /Milestone2
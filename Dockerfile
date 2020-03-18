FROM python:3.8

WORKDIR /app
COPY ./doc/requirements/base.txt /app/doc/requirements/
RUN pip install -r ./doc/requirements/base.txt
COPY . /app/

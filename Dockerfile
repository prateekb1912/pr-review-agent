FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y parallel

RUN pip install -r requirements.txt

COPY . .

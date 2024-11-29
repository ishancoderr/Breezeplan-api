FROM python:3.11-slim

WORKDIR /app

COPY . /app

COPY requirement.txt .
RUN pip install -r requirement.txt

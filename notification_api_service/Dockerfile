FROM python:3.10-slim

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir

EXPOSE 8001

COPY ./source .
COPY ./entrypoint.sh .

RUN apt update && apt install -y netcat && chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh && python main.py

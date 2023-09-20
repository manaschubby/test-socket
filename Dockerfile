# syntax=docker/dockerfile:1
FROM python:3.10-slim

COPY *.py /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn","--timeout","0", "--bind", "0.0.0.0:9000", "socket_server:app"]

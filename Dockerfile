FROM python:3.8-slim

RUN apt-get update && apt-get install -y git gcc libpcre3-dev poppler-utils tesseract-ocr tesseract-ocr-spa tesseract-ocr-cat antiword
RUN pip install pip==24.0

COPY requirements.txt requirements-dev.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app/
WORKDIR /app

ENV FLASK_APP=scanner_backend/app.py

CMD gunicorn --access-logfile - scanner_backend.wsgi:app

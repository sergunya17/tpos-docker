FROM python:3.9.0-buster
WORKDIR /flask_app/
COPY flask_app.py .
COPY requirements.txt .
RUN pip install -q -r requirements.txt && apt-get -q update && apt-get -qy install netcat

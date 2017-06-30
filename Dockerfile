FROM python:2.7-slim

WORKDIR /bluefields_unicef

ADD  . /bluefields_unicef

RUN pip install -r requirements.txt

EXPOSE 8000

ENV APIRAPIDPRO www.rapidpro.com

ENTRYPOINT gunicorn -b 0.0.0.0:8000 -w 4 unicef_app.wsgi

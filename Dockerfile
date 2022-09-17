# syntax=docker/dockerfile:1

FROM python:3.10.7-slim-buster

WORKDIR /map

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "--app" , "smartographer", "run", "--host=0.0.0.0"]

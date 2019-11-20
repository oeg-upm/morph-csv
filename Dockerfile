FROM ubuntu:18.04

RUN apt-get update && apt-get install -y nodejs npm wget python3 bc vim build-essential python3-pip openjdk-8-jdk

RUN npm i -g @rmlio/yarrrml-parser

RUN mkdir /morph-csv

COPY . /morph-csv

RUN pip install -r /morph-csv/requirements.txt

CMD ["tail", "-f", "/dev/null"]
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y nodejs npm wget python3 bc vim build-essential python3-pip openjdk-8-jdk

RUN npm i -g @rmlio/yarrrml-parser
RUN npm -g install sparqljs
RUN mkdir /morphcsv && mkdir /results && mkdir /data && mkdir /mappings && mkdir /queries

COPY . /morphcsv

RUN pip3 install -r /morphcsv/requirements.txt

CMD ["tail", "-f", "/dev/null"]

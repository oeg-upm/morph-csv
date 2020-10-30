FROM ubuntu:18.04

RUN apt-get update && apt-get install -y nodejs npm wget unzip zip python3 bc vim build-essential python3-pip openjdk-8-jdk

RUN npm i -g @rmlio/yarrrml-parser
RUN npm -g install sparqljs
RUN mkdir /morphcsv && mkdir /results && mkdir -p /data/bsbm && mkdir /mappings && mkdir /queries

COPY bash /morphcsv/bash
COPY clean /morphcsv/clean
#COPY evaluation /morphcsv/evaluation
COPY normalization /morphcsv/normalization
COPY selection /morphcsv/selection
COPY schema_generation /morphcsv/schema_generation
COPY utils /morphcsv/utils
COPY morph-csv-interface/backend /server
COPY morph-csv-interface/morph-rdb /morph-rdb
ADD requirements.txt /morphcsv/
ADD morphcsv.py /morphcsv/
ADD debug.py /morphcsv/

RUN pip3 install -r /morphcsv/requirements.txt
#RUN bash /morphcsv/evaluation/preparation.sh
EXPOSE 5000
CMD ["python3", "/server/app.py"]

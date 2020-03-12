FROM ubuntu:18.04

RUN apt-get update && apt-get install -y openjdk-8-jdk nano less git maven bc
RUN mkdir /morphcsv
RUN mkdir /results
RUN mkdir /data
RUN mkdir /mappings
RUN mkdir /morphcsv/queries
RUN mkdir /morphcsv/output
COPY . /morphcsv

RUN cd /morphcsv && mvn clean compile assembly:single && cp target/morph-csv-1.0-jar-with-dependencies.jar morph-csv.jar

RUN cp /morphcsv/run.sh /run.sh
RUN cp /morphcsv/evaluate.sh /evaluate.sh
RUN cp /morphcsv/config.json /config.json

CMD ["tail", "-f", "/dev/null"]

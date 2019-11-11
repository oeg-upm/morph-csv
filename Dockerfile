FROM ubuntu:18.04

RUN apt-get update && apt-get install -y nodejs npm python3 bc vim build-essential python3-pip

RUN npm i -g @rmlio/yarrrml-parser

RUN pip install -r requirements.txt



CMD ["tail", "-f", "/dev/null"]
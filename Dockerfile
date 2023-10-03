FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3.10  python3-pip 

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src/  /src

WORKDIR /src/

ENTRYPOINT  [ "python3", "main.py" ]
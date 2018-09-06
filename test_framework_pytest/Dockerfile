FROM python:3.6
#FROM ubuntu:latest

MAINTAINER kalistratovka@nis-glonass.ru

ADD pytest /nis-test

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get install ca-certificates -y
RUN apt-get update
#RUN apt-get install librdkafka-dev -y
RUN apt install net-tools -y
RUN apt install telnet -y
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install kafka
RUN pip install kazoo
RUN pip install zc.zk
RUN pip install pytest
RUN pip install pytest-allure-adaptor
RUN pip install psycopg2
RUN pip install jsondiff
RUN pip install lxml
RUN pip install xmldiff
RUN pip install xml_diff
RUN pip install PyHamcrest
RUN pip install pprint
RUN pip install avro
RUN apt install default-jdk -y
RUN pip install confluent-kafka
RUN pip install confluent-kafka[avro]
RUN pip install fastavro
RUN pip install numexpr
RUN pip install ConfigParser
#RUN pip install allure-pytest
RUN pip install SQLAlchemy
RUN pip install allure-python-commons
RUN pip install testrail
RUN pip install pytest_testrail



WORKDIR /nis-test

ENTRYPOINT [ "/bin/sh", "/nis-test/bin/sleep.sh" ]
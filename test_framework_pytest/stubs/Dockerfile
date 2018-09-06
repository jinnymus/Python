#FROM python:2
FROM repo.nis-glonass.ru/base_images/basic_test:python2

MAINTAINER kalistratovka@nis-glonass.ru

RUN mkdir -p /app

COPY ./ /app

RUN ls /app

WORKDIR /app

#ENTRYPOINT [ "/bin/sh", "/app/server_gmlc.py /app false" ]
ENTRYPOINT [ "/bin/sh", "/app/sleep.sh" ]

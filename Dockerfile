# This dockerfile is used to build bma_backend

ARG BUILD_DATE
ARG VCS_REF

#Pull base image
FROM python:3.12.1

LABEL name="Aravind Allu" email="alluaravind1313@gmail.com"
LABEL description="Used for creating a container which helps to host a backend server for the bma application"

ADD . /code/
WORKDIR /code
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN pip3 install -r ./requirements/test.txt

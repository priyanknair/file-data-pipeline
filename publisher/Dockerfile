FROM python:3.10
RUN mkdir -p /publisher
WORKDIR /publisher

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install system dependencies
RUN apt update
RUN apt -y install build-essential libwrap0-dev libssl-dev libc-ares-dev uuid-dev xsltproc
RUN apt-get update -qq
RUN apt-get install --no-install-recommends --yes build-essential gcc python3-dev mosquitto mosquitto-clients musl-dev libffi-dev

RUN  ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/timezone && \
     ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime

COPY requirements.txt /publisher/
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
# Copy Project
COPY . .
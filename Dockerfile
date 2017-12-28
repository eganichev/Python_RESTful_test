FROM python:3.5.2
ENV src /backend-src

RUN apt-get update
RUN apt-get install -y python-pip python-dev libmysqlclient-dev

COPY . ${src}
WORKDIR ${src}

RUN pip install -r requirements.txt

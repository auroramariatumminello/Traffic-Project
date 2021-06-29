FROM python:3.8

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /scripts

#COPY run.sh .

ADD py /scripts/

ENV PYTHONPATH /scripts

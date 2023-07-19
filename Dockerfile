FROM ubuntu:18.04
RUN apt-get update && apt-get -y update

RUN apt-get -y update \
    && apt-get install -y wget \
    && apt-get install -y jq \
    && apt-get install -y lsb-release \
    && apt-get install -y openjdk-8-jdk-headless \
    && apt-get install -y build-essential python3-pip \
    && pip3 -q install pip --upgrade \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
         /usr/share/man /usr/share/doc /usr/share/doc-base

ENV PYSPARK_DRIVER_PYTHON=python3
ENV PYSPARK_PYTHON=python3

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 8515
WORKDIR /code/fast-api-basics
COPY . .

RUN pip install -r requirements.txt


ENV PYTHONUNBUFFERED=1 \
  PYTHONPATH=/code/fast-api-basics/app \
  PORT=5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
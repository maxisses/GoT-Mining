FROM tensorflow/tensorflow:1.15.0-gpu-py3

RUN apt-get -y update && apt-get -y install gcc

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /
COPY checkpoint /checkpoint
COPY app.py /

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8081

ENTRYPOINT ["python3", "-X", "utf8", "app.py"]

FROM tensorflow/tensorflow:1.15.0-gpu-py3

RUN apt-get -y update && apt-get -y install gcc

COPY requirements-docker.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /
COPY GoT_textonly.txt /GoT_textonly.txt
##models will be downloaded by the running container according to below modelsize
COPY models /models
COPY app.py /

ENV MODELSIZE="124M"

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["python3", "-X", "utf8", "-u", "app.py"]

##makes a multistage build - takes VERY long as it cant use GPUs
FROM tensorflow/tensorflow:1.15.0-gpu-py3 AS trainmodel

RUN apt-get -y update && apt-get -y install gcc

COPY gpt2-model-training/requirements-docker.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /
COPY gpt2-model-training/GoT_textonly.txt /GoT_textonly.txt
##models will be downloaded by the running container according to below modelsize
COPY gpt2-model-training/models /models
COPY gpt2-model-training/app.py /

ENV MODELSIZE="124M"

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN python3 -X utf8 -u app.py

FROM tensorflow/tensorflow:1.15.0-gpu-py3 as runmodel

RUN apt-get -y update && apt-get -y install gcc

COPY gpt2-model-inferencing/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /
COPY --from=trainmodel checkpoint /checkpoint
COPY gpt2-model-inferencing/app.py /

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PORT 8080

EXPOSE 8080

ENTRYPOINT ["python3", "-X", "utf8", "-u", "app.py"]


FROM registry.access.redhat.com/ubi8/python-36

RUN apt-get -y update && apt-get -y install gcc wget unzip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /

## either place in the tensorflow checkpoint in this directory or use trained model from object store
# COPY checkpoint /checkpoint
RUN wget --show-progress https://s3.us.cloud-object-storage.appdomain.cloud/gameofthronesmining-donotdelete-pr-cooghodv8gdsbq/checkpoint.zip \
    && unzip checkpoint.zip && rm checkpoint.zip

COPY app.py /
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PORT 8080

EXPOSE 8080

ENTRYPOINT ["python3", "-X", "utf8", "-u", "app.py"]

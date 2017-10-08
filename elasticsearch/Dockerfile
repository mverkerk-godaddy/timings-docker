FROM docker.elastic.co/elasticsearch/elasticsearch:5.6.2

LABEL Description="docker_es"

ENV PORT 9200
EXPOSE 9200

# pip used to install request - for Kibana import
USER root
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
RUN pip install requests

USER elasticsearch
ADD import ./import
FROM alpine:latest

RUN  apk update && apk add git \
    nano \
    python3 \
    elasticsearch
RUN git clone https://github.com/EricKrg/FlyPy.git && cd FlyPy && ls && pip3 install -r req.txt
EXPOSE 9200
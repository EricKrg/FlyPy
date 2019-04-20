FROM ubuntu:latest
RUN  apt-get update && apt-get install git \
    nano \
    python3 \
    python3-pip \
    openjdk-8-jdk \
    apt-transport-https \
    wget \
    software-properties-common \
    gnupg2 -y
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN add-apt-repository "deb https://artifacts.elastic.co/packages/6.x/apt stable main"
RUN apt-get update && apt-get install elasticsearch
RUN git clone https://github.com/EricKrg/FlyPy.git && cd FlyPy && ls && pip3 install -r req.txt
RUN cd FlyPy && cat config >> /etc/elasticsearch/elasticsearch.yml && cat java_home >> /etc/environment
RUN service elasticsearch start
EXPOSE 9200
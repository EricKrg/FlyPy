FROM elasticsearch:5.6-alpine
RUN  apk update && apk add git \
    nano \
    python3
RUN git clone https://github.com/EricKrg/FlyPy.git && cd FlyPy && ls && pip3 install -r req.txt
RUN cd FlyPy && python3 migrate.py
EXPOSE 9200
FROM alpine:latest
RUN apk update && apk add git \
    python3
RUN git clone https://github.com/EricKrg/FlyPy.git && cd FlyPy && ls && pip3 install -r req.txt
EXPOSE 5000
CMD cd FlyPy; python3 app.py

FROM alpine:latest

RUN  apk update && apk add openjdk8 \
    git \
    nano \
    python3
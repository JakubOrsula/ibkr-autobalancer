## Custom Dockerfile
FROM consol/ubuntu-xfce-vnc
ENV REFRESHED_AT 2018-08-21

## Install
USER 0
RUN apt-get update && apt-get install -y openjdk-8-jre curl \
    && apt-get clean -y

WORKDIR /headless/Downloads
RUN curl -o ibgateway-latest.sh https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-linux-x64.sh \
    chmod +rx ibgateway-latest.sh

USER 1000
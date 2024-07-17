FROM ubuntu:jammy

WORKDIR /app
RUN apt update && apt install -y wget sudo software-properties-common \
    python3-pip python3-wheel
RUN sudo add-apt-repository ppa:robotraconteur/ppa -y \
    && sudo apt-get update \
    && sudo apt-get install python3-robotraconteur -y

RUN python3 -m pip install --upgrade pip

COPY . ./
RUN python3 -m pip install .

COPY ./config/*.yml /config/

ENV SENSOR_INFO_FILE=/config/generic_cognex_sensor_default_config.yml

CMD python3 -m cognex_robotraconteur_driver --sensor-info-file=$SENSOR_INFO_FILE

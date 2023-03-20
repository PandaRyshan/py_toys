FROM ubuntu:jammy
LABEL maintainer="Hu Xiaohong <xiaohong@duckduck.io>"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY ./src/ /src/

WORKDIR /src

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libasound2 \
        wget \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl-dev_1.1.1f-1ubuntu2.17_amd64.deb \
    && dpkg -i libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb \
    && dpkg -i libssl-dev_1.1.1f-1ubuntu2.17_amd64.deb \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb \
    && rm -f libssl-dev_1.1.1f-1ubuntu2.17_amd64.deb \
    && pip install -e .[prod] \
    && flask init-db

CMD [ "flask", "run" ]
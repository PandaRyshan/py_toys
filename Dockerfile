FROM ubuntu:jammy
LABEL maintainer="Hu Xiaohong <xiaohong@pandas.run>"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG LIB_VERSION=1.1_1.1.1f-1ubuntu2.20_amd64

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libasound2 \
        wget \
        python3.10 \
        python3-pip \
        python3-venv \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl${LIB_VERSION}.deb \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl-dev_${LIB_VERSION}.deb \
    && dpkg -i libssl${LIB_VERSION}.deb \
    && dpkg -i libssl-dev_${LIB_VERSION}.deb \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f libssl${LIB_VERSION}.deb \
    && rm -f libssl-dev_${LIB_VERSION}.deb

WORKDIR /py_toys

COPY . .

RUN set -x \
    && pip install -e .[prod]

CMD flask init-db && gunicorn -c gunicorn.conf.py 'src:create_app()'
# CMD [ "flask", "run" ]

EXPOSE 8000

# file: 3dspeaker.Dockerfile

FROM docker.io/library/python:3.9-slim-bullseye

ARG PIP_INDEX_URL=http://oa-mirror.mediatek.inc/repository/pypi/simple
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cu118

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONHTTPSVERIFY=0
ENV PATH=/opt/3dspeaker_venv/bin:$PATH

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        vim \
        tmux \
        unzip \
        libaio-dev \
        pdsh \
        ccache \
        build-essential \
        cmake \
        zlib1g-dev \
        libbz2-dev \
        liblzma-dev \
        libsndfile1 \
        net-tools \
        iperf3 \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/3dspeaker_venv

RUN pip config set global.index-url ${PIP_INDEX_URL} \
    && pip config set global.trusted-host oa-mirror.mediatek.inc \
    && pip config set global.no-cache-dir true

RUN pip install --upgrade "pip<25" "setuptools<70" wheel

COPY 3dspeaker_requirements.txt /tmp/3dspeaker_requirements.txt

RUN pip install --no-build-isolation -r /tmp/3dspeaker_requirements.txt

RUN pip install \
    --index-url ${TORCH_INDEX_URL} \
    --trusted-host download.pytorch.org \
    --trusted-host download-r2.pytorch.org \
    torch==2.4.1 \
    torchaudio==2.4.1

WORKDIR /workspace

ENV PYTHONPATH=/workspace:$PYTHONPATH

ENTRYPOINT []


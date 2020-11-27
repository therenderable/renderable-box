FROM ubuntu:20.04

LABEL description "Renderable container image."
LABEL version "1.0.0"
LABEL maintainer "Danilo Peixoto <danilo@therenderable.com>"

ENV CONTAINER_NAME "renderable-box"
ENV PYTHON_VERSION "3.7.0"

WORKDIR /usr/src/renderable-box/
COPY . .

RUN apt-get update && apt-get install -y \
  wget \
  zip \
  build-essential \
  zlib1g-dev \
  libncurses5-dev \
  libgdbm-dev \
  libnss3-dev \
  libssl-dev \
  libreadline-dev \
  libffi-dev

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
  && tar -xvzf Python-${PYTHON_VERSION}.tgz \
  && cd Python-${PYTHON_VERSION} \
  && ./configure --enable-optimizations \
  && make install . \
  && cd .. \
  && rm -rf Python-${PYTHON_VERSION}.tgz \
	&& rm -rf Python-${PYTHON_VERSION}

RUN pip3 install --upgrade pip
RUN pip3 install .

CMD ["renderable-box"]

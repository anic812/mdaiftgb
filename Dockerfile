FROM ubuntu:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US:en TZ=Asia/Kolkata

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    libcurl3-gnutls \
    libmms0 \
    libzen0v5 \
    libcurl4-gnutls-dev \
    libzen-dev \
    wget \
    ffmpeg \
    libsox-fmt-mp3 \
    sox \
    locales \
    megatools \
    software-properties-common \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
   && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-distutils

# Install pip for Python 3.11
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py
 

RUN wget -q -O /tmp/libmediainfo0v5.deb https://mediaarea.net/download/binary/libmediainfo0/24.06/libmediainfo0v5_24.06-1_amd64.Ubuntu_24.04.deb \
  && dpkg -i /tmp/libmediainfo0v5.deb \
  && rm /tmp/libmediainfo0v5.deb

RUN wget -q -O /tmp/libtinyxml2-9.deb http://th.archive.ubuntu.com/ubuntu/pool/universe/t/tinyxml2/libtinyxml2-9_9.0.0+dfsg-3.1_amd64.deb \
  && dpkg -i /tmp/libtinyxml2-9.deb \
  && rm /tmp/libtinyxml2-9.deb

RUN wget -q -O /tmp/mediainfo.deb https://mediaarea.net/download/binary/mediainfo/24.06/mediainfo_24.06-1_amd64.Ubuntu_24.04.deb \
  && dpkg -i /tmp/mediainfo.deb \
  && rm /tmp/mediainfo.deb

RUN locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

CMD ["bash", "start.sh"]

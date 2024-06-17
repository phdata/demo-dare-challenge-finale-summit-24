FROM  --platform=linux/amd64 debian:11.1-slim
#FROM --platform=linux/amd64 nvcr.io/nvidia/pytorch:24.04-py3

# ENVIRONMENT VARIABLES
ENV DISPLAY=:1 \
    VNC_PORT=5901 \
    NO_VNC_PORT=8080 \
    VNC_COL_DEPTH=32 \
    VNC_RESOLUTION=1024x768 \
    DEBIAN_FRONTEND=noninteractive \
    TERM=xterm \
    TIGER_VNC_PASSWORD=PASSWORD

# INSTALL DEPENDENCIES
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    xvfb xauth xterm \
    wget sudo git bzip2 python3 ca-certificates \
    imagemagick \
    python3-pip \
    python-is-python3 \
    firefox-esr \
    tigervnc-standalone-server tigervnc-common \
    build-essential \
    libsdl2-dev \
    libsdl2-net-dev \
    libsdl2-mixer-dev \
    python3-pil \
    automake \
    autoconf \
    libtool \
    pkg-config

RUN python3 -m pip install flask numpy jupyterlab snowflake

# GET NOVNC
RUN git clone --branch v1.2.0 --single-branch https://github.com/novnc/noVNC.git /opt/noVNC; \
    git clone --branch v0.9.0 --single-branch https://github.com/novnc/websockify.git /opt/noVNC/utils/websockify; \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# CLONE CRISPY-DOOM REPOSITORY
WORKDIR /opt
RUN git clone https://github.com/fabiangreffrath/crispy-doom.git

# RUN COMPILATION COMMANDS
WORKDIR /opt/crispy-doom
RUN autoreconf -fiv && \
    ./configure && \
    make && \
    make install

# GET DOOM1 WAD FILE
RUN wget -O doom1.wad http://ftp.debian.org/debian/pool/non-free/d/doom-wad-shareware/doom-wad-shareware_1.9.fixed.orig.tar.gz && \
    tar -xzvf doom1.wad && \
    mv /opt/crispy-doom/doom-wad-shareware-1.9.fixed/doom1.wad /opt/crispy-doom && \
    rm -rf /opt/crispy-doom/doom-wad-shareware-1.9.fixed

# CLEANUP
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /src
COPY . /src
COPY crispy-doom.cfg /opt/crispy-doom/
COPY default.cfg /opt/crispy-doom/
COPY screenshot_sync.py /opt/crispy-doom/

EXPOSE 5901 8080
ENTRYPOINT ["/src/entrypoint.sh"]

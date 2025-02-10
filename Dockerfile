# Dockerfile for providing buildozer

FROM ubuntu:22.04

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/hostcwd" \
    SRC_DIR="${HOME_DIR}/src" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

# Configure locale
RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# Install system dependencies
RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    autoconf \
    automake \
    build-essential \
    ccache \
    cmake \
    gettext \
    git \
    libffi-dev \
    libltdl-dev \
    libssl-dev \
    libtool \
    openjdk-17-jdk \
    patch \
    pkg-config \
    python3-pip \
    python3-setuptools \
    sudo \
    unzip \
    zip \
    zlib1g-dev \
    && apt clean && rm -rf /var/lib/apt/lists/*  # Reduce image size

# Prepare non-root environment
RUN useradd --create-home --shell /bin/bash ${USER}
RUN usermod -aG sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}
WORKDIR ${WORK_DIR}
COPY --chown=user:user requirements.txt ${SRC_DIR}/requirements.txt
COPY --chown=user:user . ${SRC_DIR}

# Install Buildozer and dependencies
RUN pip3 install --upgrade "Cython<3.0" wheel pip
RUN test -f ${SRC_DIR}/requirements.txt && pip3 install --no-cache-dir -r ${SRC_DIR}/requirements.txt || echo "No requirements.txt found, skipping..."

# Fix permissions issue with .buildozer
RUN mkdir -p ${HOME_DIR}/.buildozer && chmod -R 777 ${HOME_DIR}/.buildozer

# Disable BuildKit to avoid OCI image format issues
ENV DOCKER_BUILDKIT=0

ENTRYPOINT ["buildozer"]

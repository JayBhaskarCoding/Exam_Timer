# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/hostcwd"
ENV SRC_DIR="${HOME_DIR}/src"

# Set PATH to include user-installed binaries
ENV PATH="${HOME_DIR}/.local/bin:${PATH}"

# Install system dependencies
RUN apt update -qq > /dev/null && \
    DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    locales autoconf automake build-essential ccache cmake gettext git libffi-dev \
    libltdl-dev libssl-dev libtool openjdk-17-jdk patch pkg-config python3-pip \
    python3-setuptools sudo unzip zip zlib1g-dev && \
    locale-gen en_US.UTF-8

# Set locale
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# Create a non-root user and set permissions
RUN useradd --create-home --shell /bin/bash ${USER} && \
    usermod -append --groups sudo ${USER} && \
    echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch to the non-root user
USER ${USER}
WORKDIR ${WORK_DIR}

# Copy source files
COPY --chown=user:user . ${SRC_DIR}

# Install Buildozer and dependencies
# Install Buildozer properly
RUN pip3 install --user --upgrade buildozer
ENV PATH="/home/user/.local/bin:$PATH"

# Ensure Buildozer is installed and accessible
RUN echo "export PATH=\$HOME/.local/bin:\$PATH" >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# Use Bash as the entrypoint
ENTRYPOINT ["/bin/bash", "-c"]

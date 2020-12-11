FROM amd64/debian:10-slim
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y \
        python3 python3-yaml python3-pip && \
    apt-get clean
WORKDIR /scripts
ADD scripts .

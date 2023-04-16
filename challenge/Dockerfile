FROM ubuntu:20.04
RUN export DEBIAN_FRONTEND=noninteractive && apt update -y && apt -y install xinetd python3 python3-pip

RUN useradd ctf && \
    pip install ecdsa pycryptodome

WORKDIR /app

RUN chown ctf /app

COPY source.py .
COPY flag.py .
COPY ctf.xinetd /etc/xinetd.d/ctf

CMD xinetd -dontfork
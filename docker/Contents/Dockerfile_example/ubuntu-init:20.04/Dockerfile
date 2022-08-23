FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Seoul

RUN sed -i 's/kr.archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt update \
  && apt install -qq -y init systemd \
  && apt install -qq -y build-essential \
  && apt install -qq -y tzdata \
  && apt install -qq -y vim curl \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/{apt,dpkg,cache,log}

CMD ["/sbin/init"]
ARG AIRFLOW_BASE_IMAGE="apache/airflow:2.3.3-python3.8"

FROM ${AIRFLOW_BASE_IMAGE}

USER root
RUN apt-get update
RUN apt-get install openssh-server -y
RUN apt-get install vim -y
RUN apt-get install net-tools -y
RUN apt-get install git -y
RUN apt-get install python3 pip -y
RUN apt-get install libaio1 -y
RUN apt-get install wget -y
RUN apt-get install unzip -y

RUN echo "alias ll='ls --color=auto -alF'" >> ~/.bashrc
RUN source ~/.bashrc


# Oracle-client 실행을 위한 설치 
WORKDIR /opt/oracle
RUN wget --no-check-certificate https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

# python 외부 패키지 설치
WORKDIR /opt/airflow
USER airflow
COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

USER airflow

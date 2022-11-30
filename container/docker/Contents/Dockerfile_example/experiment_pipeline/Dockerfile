########## Configuration Begin ############

ARG ANACONDA_VERSION=2020.11
ARG TENSORFLOW_VERSION=2.6.2
ARG PYTORCH_VERSION=1.10.0
ARG PYTHON_VERSION=3.8
ARG ML_TYPE=cpu

ARG AIRFLOW_BASE_IMAGE="apache/airflow:2.3.3-python${PYTHON_VERSION}"

########### Configuration End ###############

FROM ${AIRFLOW_BASE_IMAGE}

# change the root password
USER root
RUN echo "root:root!23" | chpasswd

########### Install OS dependencies ##########
RUN apt-get update
RUN apt-get install openssh-server -y
RUN apt-get install vim -y
RUN apt-get install net-tools -y
RUN apt-get install git -y
RUN apt-get install python3 pip -y
RUN apt-get install libaio1 -y
RUN apt-get install wget -y
RUN apt-get install unzip -y
RUN apt-get install ca-certificates -y

############ Configure Container Environment ############

ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash

ENV PATH=$CONDA_DIR/bin:$PATH

ENV TZ=Asia/Seoul

ADD . /tmp

# Install Jupyterhub
RUN pip install --no-cache-dir sudospawner jupyterhub && \
    apt-get install -y nodejs && \
    jupyter-notebook --generate-config && \
    mkdir -p /etc/jupyterhub && mv /tmp/jupyterhub_config.py /etc/jupyterhub/ && \
    mkdir -p /etc/pki/jupyterhub && mv /tmp/jupyter.* /etc/pki/jupyterhub/ && \
    apt-get update -y && \
    apt-get clean all && apt-get cache clean --force &&  \
    rm -fr /root/.cache /root/.npm /tmp/* /var/cache/yum/*


# Install oracle-client
WORKDIR /opt/oracle
RUN wget --no-check-certificate https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

# install python dependencies 
WORKDIR /opt/airflow
USER airflow
COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# Install jupyterhub

EXPOSE 8080 8888 22

USER airflow
RUN airflow db init 
RUN airflow users create --username airflow --password airflow  --firstname Anonymous --lastname Admin  --role Admin --email admin@example.org
CMD airflow webserver & airflow scheduler
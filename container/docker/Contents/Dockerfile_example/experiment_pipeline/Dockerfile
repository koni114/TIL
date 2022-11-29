#################### Configuration Begin ##############################

# Base Container Image
FROM nvidia/cuda:11.3.1-cudnn8-devel-centos7

# Anaconda & Python version config
ARG ANACONDA_VERSION=2020.11
#ARG PYTHON_VERSION=3.7

# Tensorflow version config - comment below if you don't want to install tensorflow
ARG TENSORFLOW_VERSION=2.6.2

# Pytorch version config - comment below if you don't want to install pytorch
ARG PYTORCH_VERSION=1.10.0

# Specify framework type. You can set type 'gpu' or 'cpu'
# type 'gpu' will install tensorflow-gpu and cudatoolkit
ARG ML_TYPE=gpu

#################### Configuration End ##############################

LABEL maintainer="Heo Jae Hun"


# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root
RUN echo "root:1234" | chpasswd

# Install OS dependencies
ADD nodesource-el7.repo /etc/yum.repos.d/
RUN yum-config-manager --quiet --disable cuda nvidia-ml > /dev/null && \
    yum install -y bzip2 wget sudo ca-certificates vim net-tools zlib zlib-devel openssl openssl-devel epel-release opencv opencv-devel opencv-python && \
    yum install -y supervisor && \
    yum update -y && \
    yum clean all && rm -rf /var/cache/yum/*

# Configure Container Environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    LC_ALL=en_US.UTF8 \
    LANG=en_US.UTF8 \
    LANGUAGE=en_US.UTF8

ENV PATH=$CONDA_DIR/bin:$PATH \
    LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

ENV TZ=Asia/Seoul

RUN echo "export PATH=/opt/conda/bin:$PATH" >> /etc/profile
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Copy a permission script
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
    cp -a /etc/skel/.bashrc /root/


# Install Anaconda
WORKDIR /tmp

RUN curl -k -o /tmp/Anaconda3-${ANACONDA_VERSION}-Linux-x86_64.sh https://repo.anaconda.com/archive/Anaconda3-${ANACONDA_VERSION}-Linux-x86_64.sh  && \
    /bin/bash Anaconda3-${ANACONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Anaconda3-${ANACONDA_VERSION}-Linux-x86_64.sh && \
    conda config --set ssl_verify false && \
    conda config --system --prepend channels conda-forge && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda config --system --set channel_priority flexible && \
    #conda config --system --set channel_priority strict && \
    if $PYTHON_VERSION; then conda install --quiet --yes python=$PYTHON_VERSION; fi && \
    conda list python | grep '^python ' | tr -s ' ' | cut -d '.' -f 1,2 | sed 's/$/.*/' >> $CONDA_DIR/conda-meta/pinned && \
    conda install --update-deps --quiet --yes conda && \
    conda install --quiet --yes pip && \
    conda update --all --quiet --yes && \
    conda clean --yes --all && \
    rm -rf /root/.cache /tmp/*


# Install Tensorflow(gpu type)
RUN if [ "$ML_TYPE" = "gpu" -a $TENSORFLOW_VERSION ]; then \
    conda config --set ssl_verify false && \
    conda install --quiet --yes tensorflow-gpu=$TENSORFLOW_VERSION && \
    conda update --all --quiet --yes && \
    conda clean --yes --all; \
    fi

# Install Tensorflow(cpu type)
RUN if [ "$ML_TYPE" = "cpu" -a $TENSORFLOW_VERSION ]; then \
    conda config --set ssl_verify false && \
    conda install --quiet --yes tensorflow=$TENSORFLOW_VERSION && \
    conda update --all --quiet --yes && \
    conda clean --yes --all; \
    fi

#RUN conda config --set ssl_verify false && \
#    conda install --quiet --yes pytorch=$PYTORCH_VERSION torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=11.3 cudnn -c pytorch -c conda-forge && \
#    conda update --all --quiet --yes && \
#    conda clean --yes --all

# Install Pytorch(gpu type)
#RUN if [ "$ML_TYPE" = "gpu" -a $PYTORCH_VERSION ]; then \
#    conda config --set ssl_verify false && \
#    conda install --quiet --yes pytorch=$PYTORCH_VERSION torchvision cudatoolkit -c pytorch -c conda-forge && \
#    conda update --all --quiet --yes && \    
#    conda clean --yes --all; \
#    fi

# Install Pytorch cpu-type
#RUN if [ "$ML_TYPE" = "cpu" -a $PYTORCH_VERSION ]; then \
#    conda config --set ssl_verify false && \
#    conda install --quiet --yes pytorch=$PYTORCH_VERSION torchvision -c pytorch -c conda-forge && \
#    conda update --all --quiet --yes && \
#    conda clean --yes --all; \
#    fi


ADD . /tmp

# Install addtional_packages
RUN if grep -E -v '^$|^#' additional_packages.txt; then \
    conda config --set ssl_verify false && \
    conda install --quiet --yes --file additional_packages.txt && \
    pip install --no-cache-dir --upgrade opencv-contrib-python opencv-python==4.5.2.52 kaleido pygame ray==1.6.0 caserecommender spotlight datetime2 pickle5 torchsummary pytorch-tabnet && \
    pip install --no-cache-dir pathlib jsonpatch daal==2021.4.0.0 && \
    pip install --no-cache-dir lightgbm --install-option=--gpu && \
    conda update --all --quiet --yes && \
    conda clean --yes --all; \
    fi


# Install Portable Openssh and Supervisord
RUN groupadd -g 74 sshd && \
    useradd -u 74 -g sshd -d /var/empty/sshd -s /sbin/nologin -c "Privilege-separated SSH" sshd

RUN cd /tmp && \
    tar -xvzf openssh-8.6p1.tar.gz && \
    cd openssh-8.6p1 && ./configure && make -j && make install && make host-key && \
    mv /tmp/svc.ini /etc/supervisord.d/ && \
    mv /tmp/userconfig.sh /etc/rc.d/init.d/userconfig && \
    mv /tmp/nodesource-el7.repo /etc/yum.repos.d/ && \
    rm -rf /var/cache/yum/* /tmp/openssh* /tmp/userconfig.sh


## User Configuration
RUN sed -i -e '/PermitRootLogin/a\PermitRootLogin yes' /usr/local/etc/sshd_config && \
    sed -i -e '/pidfile/a\user=root' -e 's/nodaemon=false/nodaemon=true/' /etc/supervisord.conf


# Install Jupyterhub
RUN pip install --no-cache-dir sudospawner jupyterhub && \
    yum install -y nodejs && \
    npm config set strict-ssl false && \ 
    npm install -g configurable-http-proxy@4.3.2 && \
    jupyter-notebook --generate-config && \
    mkdir -p /etc/jupyterhub && mv /tmp/jupyterhub_config.py /etc/jupyterhub/ && \
    mkdir -p /etc/pki/jupyterhub && mv /tmp/jupyter.* /etc/pki/jupyterhub/ && \
    yum update -y && \
    yum clean all && npm cache clean --force &&  \
    rm -fr /root/.cache /root/.npm /tmp/* /var/cache/yum/*
 
# Group & User configration
#RUN echo "root:dlatl0!$" | chpasswd
RUN groupadd -g 983 docker && \
    useradd -u 10009 -g docker -m -d /home/testuer -s /bin/bash testuser && echo "testuser:1234" | chpasswd 

WORKDIR /

EXPOSE 8888 22

CMD [ "/usr/bin/supervisord" ]
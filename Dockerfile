FROM amazonlinux:latest

RUN yum -y install \
    python3 \
    python3-pip \
    zip \
    && yum clean all

WORKDIR /var/task

COPY lambda_layer/requirements.txt .

RUN pip3 install -r requirements.txt -t python/lib/python3.13/site-packages/

FROM centos:7

RUN yum install -y git epel-release python-pip net-tools ansible docker-client
# we don't need intstall docker whole package just we need docker-clinet from extra repo
# RUN yum install -y yum-utils
# RUN yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
# RUN yum install -y docker-ce

COPY dcos_generate_config.ee.sh /dcos/dcos_generate_config.ee.sh

RUN git clone https://github.com/sorididim11/dcos-ansible-terraform.git
WORKDIR dcos-ansible-terraform


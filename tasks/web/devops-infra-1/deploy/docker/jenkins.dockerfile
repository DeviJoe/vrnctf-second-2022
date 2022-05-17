FROM jenkins/jenkins:lts

USER root
COPY --chown=root:root --chmod=400 ./files/second_flag.txt /root/second_flag.txt

RUN apt update && apt install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && apt install -y python3.9 && apt install -y pip
RUN apt install sudo 
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install ansible

RUN echo "jenkins ALL=(ALL) NOPASSWD:/usr/local/bin/ansible-playbook" >> /etc/sudoers
FROM ubuntu:18.04

MAINTAINER S. Koulouzis

ARG montage_version=v5.0

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get upgrade -y
RUN apt-get install wget build-essential -y

WORKDIR /root
RUN pwd


RUN wget http://montage.ipac.caltech.edu/download/Montage_$montage_version.tar.gz
RUN tar -xzf Montage_$montage_version.tar.gz
WORKDIR Montage
RUN make

RUN mkdir examples
COPY pleiades.sh examples
COPY pleiades.hdr examples
COPY downloadDSS.sh examples


ENV PATH=$PATH:/root/Montage/bin
RUN echo PATH=$PATH:/root/Montage/bin >> /etc/profile
RUN echo PATH=$PATH:/root/Montage/examples >> /etc/profile
RUN source /etc/profile

 
RUN echo PATH=$PATH:/root/Montage/bin >> /root/.bashrc 
RUN echo PATH=$PATH:/root/Montage/examples >> /root/.bashrc
RUN source /root/.bashrc

WORKDIR examples
RUN chmod +x *.sh
# RUN ./downloadDSS.sh
# RUN sh pleiades.sh
 
# ENTRYPOINT tail -f /dev/null
# ENTRYPOINT sh pleiades.sh > out.log 

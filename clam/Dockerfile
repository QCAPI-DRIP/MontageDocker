FROM alogo53/montage:5.0

RUN apt-get -y update 
RUN apt-get install -y python3 python3-pip virtualenv
RUN pip3 install requests clam

WORKDIR /root

COPY mAdd mAdd/
COPY mArchiveExec mArchiveExec/
COPY mArchiveList mArchiveList/
COPY mImgtbl mImgtbl/
COPY mJPEG mJPEG/
COPY mProjExec mProjExec/

RUN virtualenv --python=python3 clamenv 
EXPOSE 8080

ENTRYPOINT source clamenv/bin/activate && pip3 install clam && cd $MONTAGE_MODULE && ./startserver_development.sh

# docker build -t montage_clam .
# docker run -e MONTAGE_MODULE=mAdd -it -h montage_clam --name clam -p 8080:8081 montage_clam

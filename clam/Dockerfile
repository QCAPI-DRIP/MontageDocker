FROM alogo53/montage:5.0

RUN apt-get install -y python3 python3-pip virtualenv
RUN pip3 install requests clam

WORKDIR /root

RUN virtualenv --python=python3 clamenv 
RUN source clamenv/bin/activate && pip3 install clam



ENTRYPOINT tail -f /dev/null #clamservice -H localhost -p 8080 clam.config.textstats

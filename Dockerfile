FROM ubuntu
RUN apt-get install -y python
RUN apt-get install -y git
RUN apt-get install -y wget 
RUN git clone https://github.com/ronpanto/do-backend.git /root/do-backend-repo
RUN wget https://www.dropbox.com/s/syyxbw3djq4k9iu/candidate.tar.gz
RUN tar -zxvf candidate.tar.gz
RUN mv package_contents /root/package_contents

EXPOSE 8080
WORKDIR /root/do-backend-repo
CMD ["/usr/bin/python", "main.py", "&"]

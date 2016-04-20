FROM ubuntu
RUN apt-get install -y python
RUN apt-get install -y git
 
RUN git clone https://github.com/ronpanto/do-backend.git /root/do-backend-repo

EXPOSE 8080
WORKDIR /root/do-backend-repo
CMD ["/usr/bin/python", "main.py", "&"]

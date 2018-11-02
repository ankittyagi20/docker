FROM centos:7
RUN yum update -y
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
RUN mkdir ~/.ssh
COPY id_rsa /root/.ssh/id_rsa
COPY config /root/.ssh/config
CMD ["chmod", "600", "/root/.ssh/id_rsa"]
RUN yum -y install git
#RUN yum -y install nginx
RUN mkdir /app
COPY execute.sh /app/
COPY app.py /app/
COPY deploy_flask.py /app/
WORKDIR /app
#ENTRYPOINT ["python"]
#CMD ["deploy_flask.py"]
#CMD ["app.py"]
#CMD ["/usr/bin/env", "sh"]
CMD ["/app/execute.sh"]

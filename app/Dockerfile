FROM centos:7
RUN yum update -y
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
COPY . /app
COPY docker_configs/ /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["deploy_flask.py"]

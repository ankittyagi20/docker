FROM centos:7
RUN yum update -y
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
#RUN pip install FLask==0.10.0
RUN mkdir /app
#COPY app.py /app/
#COPY deploy_flask.py /app/
WORKDIR /app
#CMD ["/bin/bash"]
ENTRYPOINT ["python"]
CMD ["deploy_flask.py"]
CMD ["app.py"]

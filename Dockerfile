
FROM centos:latest
RUN yum -y upgrade
RUN yum install -y python3 
RUN pip3 install flask 
RUN pip3 install psycopg2-binary
COPY emp_app.py /root/

ENTRYPOINT python3 /root/emp_app.py

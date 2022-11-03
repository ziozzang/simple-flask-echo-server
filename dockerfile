FROM python:3

RUN pip install flask psutils

COPY *.py /opt/

EXPOSE 8080
WORKDIR /opt/

CMD python server.py


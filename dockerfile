FROM python:3

RUN pip install flask psutil

COPY *.py /opt/

EXPOSE 8080
WORKDIR /opt/

CMD python server.py


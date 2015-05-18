FROM python:3.4.3

RUN apt-get update

RUN pip install cairocffi
RUN pip install nap
RUN pip install boto
RUN pip install numpy
RUN pip install Pillow

ADD ./src/* /app/

ENTRYPOINT ["python"]

CMD ["/app/main.py"]

EXPOSE 5000
FROM python:3.4.3

RUN apt-get update

RUN pip install cairocffi
RUN pip install nap
RUN pip install boto

ADD ./src/* /app/

CMD [ "python", "/app/main.py" ]

EXPOSE 5000
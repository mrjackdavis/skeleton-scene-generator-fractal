FROM python:3.4.3

RUN apt-get update

RUN pip install cairocffi
RUN pip install Flask
RUN pip install nap

ADD ./src/* /app/

CMD [ "python", "/app/main.py" ]

EXPOSE 5000
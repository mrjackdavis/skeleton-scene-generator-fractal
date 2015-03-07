FROM python:3.4.3

RUN apt-get update

RUN pip install cairocffi
RUN pip install Flask

ADD ./src/main.py /app/main.py

CMD [ "python", "/app/main.py" ]

EXPOSE 5000
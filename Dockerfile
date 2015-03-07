FROM python:3.4.3

RUN apt-get update

RUN pip install cairocffi
RUN pip install Flask

ADD ./main.py /main.py

CMD [ "python", "/main.py" ]

EXPOSE 5000
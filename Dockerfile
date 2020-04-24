FROM python:3
USER root
RUN mkdir /app
WORKDIR /app
RUN apt-get install gcc libpq-dev
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
CMD ["python3", "/app/bot.py"]


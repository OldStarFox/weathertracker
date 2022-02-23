FROM python:3.8-bullseye

WORKDIR /code

RUN mkdir /data

RUN apt update
RUN apt upgrade

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY *.py ./

EXPOSE 9877

ENTRYPOINT [ "python" ]
CMD [ "prometheus_metrics.py" ]
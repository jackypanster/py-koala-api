FROM python:3.6.4-alpine3.7

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update && apk add build-base

RUN mkdir /log

COPY config.py /
COPY main.py   /

RUN pip3 install sanic
RUN pip3 install motor

EXPOSE 8000

ENV APP_SETTINGS=config.py

CMD ["python3", "main.py" ]
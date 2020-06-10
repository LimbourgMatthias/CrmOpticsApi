FROM python:3.7-alpine

WORKDIR '/app'

RUN apk add --no-cache linux-headers g++

COPY ./ ./

RUN pip install -r requirements.txt

RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi

USER uwsgi

CMD ["uwsgi", "--ini", "app.ini"]
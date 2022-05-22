FROM python:3.10-alpine

ENV PATH="/scripts:${PATH}"

COPY requirements.txt /requirements.txt

RUN apk update && apk add  --no-cache postgresql-dev gcc python3-dev musl-dev postgresql postgresql-contrib
RUN apk add --update --no-cache --virtual .tmp libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir app
COPY ./grsmu_diplom /app

WORKDIR /app

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

USER user


CMD ["entrypoint.sh"]
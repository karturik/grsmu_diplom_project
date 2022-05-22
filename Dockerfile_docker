FROM python:3.10-alpine

ENV PATH="/scripts:${PATH}"

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers postgresql-dev python3-dev musl-dev
RUN pip install -r requirements.txt
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
RUN chown -R user:user /app/db.sqlite3
RUN chmod -R 755 /vol/web
RUN chmod -R 755 /vol/web/static
RUN chmod -R 755 /vol/web/media

USER user

CMD ["entrypoint.sh"]


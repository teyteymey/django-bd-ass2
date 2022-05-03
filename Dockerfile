FROM python:3.9.4-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers \
# Pillow dependencies
    && apk add postgresql-libs postgresql-dev libffi-dev \
       openldap-dev unixodbc-dev gcc musl-dev python3-dev \
       jpeg-dev zlib-dev libjpeg
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./app /app
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
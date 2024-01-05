FROM python:3.8-alpine3.18

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install -r requirements.txt && \
    apk del .tmp-build-deps


COPY . /app

WORKDIR /app


COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]

FROM alpine:latest
RUN apk add --no-cache python3-dev py3-pip && pip3 install --upgrade pip
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip3 install mysqlclient  
RUN apk del build-deps
WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"] 
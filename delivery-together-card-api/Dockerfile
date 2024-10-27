FROM python:alpine3.11

LABEL AUTHOR="Miguel Vega - Miguel Angel Tovar Bastidas"
LABEL EMAIL="ma.tovarb12@uniandes.edu.co"

COPY . /app/

WORKDIR /app

RUN apk update && apk upgrade
RUN apk add --no-cache build-base
RUN pip install --upgrade pip setuptools
RUN make install

EXPOSE 3007

ENTRYPOINT ["sh", "./docker/entrypoint.prod.sh"]
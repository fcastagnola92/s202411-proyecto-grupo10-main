FROM node:20-alpine as build
RUN mkdir /usr/local/nvm
USER root

RUN apk update && \
    apk upgrade && \
 apk add make g++
WORKDIR /usr/src/app
COPY . .

RUN npm install
RUN npm install -g tsc
RUN npm install -g typescript --force
RUN npm run build

RUN adduser -D -u 1001 appuser
RUN chown -R appuser:appuser /usr/src/app

USER appuser


ENTRYPOINT ["sh", "./docker/entrypoint.sh"]

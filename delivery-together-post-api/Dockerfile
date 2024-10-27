FROM golang:1.21.6-alpine AS build
LABEL AUTHOR="Pedro Capriles"
LABEL EMAIL="p.caprilespe@uniandes.edu.co"

WORKDIR /usr/src/app

RUN apk update
RUN apk add make g++ gcc

COPY . .
RUN make install

RUN make build

FROM alpine:latest

WORKDIR /root/

COPY --from=build /usr/src/app/app .

EXPOSE 3001

CMD ["./app"]
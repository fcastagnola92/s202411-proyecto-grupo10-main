# Projects

## Pipelines
<p style="text-align:center;">
<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo10/actions/workflows/evaluator_entrega1.yml/badge.svg" alt="Entrega 1" />
<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo10/actions/workflows/verificador_entrega1_ingress.yml/badge.svg" alt="Entrega 1 con ingress" />
<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo10/actions/workflows/evaluator_entrega2.yml/badge.svg" alt="Entrega 2 con ingress" />
<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202411-proyecto-grupo10/actions/workflows/evaluator_entrega3.yml/badge.svg" alt="Entrega 3 con ingress" />
</p>

## Made with

[![GO](https://img.shields.io/badge/go-50b7e0?style=for-the-badge&logo=go&logoColor=white&labelColor=000000)]()
[![JavaScript](https://img.shields.io/badge/javascript-ead547?style=for-the-badge&logo=javascript&logoColor=white&labelColor=000000)]()
[![Node.js](https://img.shields.io/badge/node.js-76c339?style=for-the-badge&logo=node.js&logoColor=white&labelColor=000000)]()
[![C#](https://img.shields.io/badge/c%23-8c39ac?style=for-the-badge&logo=csharp&logoColor=white&labelColor=000000)]()
[![Python](https://img.shields.io/badge/python-2b5b84?style=for-the-badge&logo=python&logoColor=white&labelColor=000000)]()
[![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=000000)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-2f72bc?style=for-the-badge&logo=typescript&logoColor=white&labelColor=000000)]()
[![PHP](https://img.shields.io/badge/php-7175aa?style=for-the-badge&logo=php&logoColor=white&labelColor=000000)]()
[![Symfony](https://img.shields.io/badge/Symfony-000000?style=for-the-badge&logo=symfony&logoColor=white&labelColor=000000)]()

# Global execution with docker compose

```sh
    docker compose up --build
```

## delivery-together-post-api

### How to run with docker

```sh
    # Go to the folder delivery-together-post-api
    cd delivery-together-post-api

    # Execute docker compose
    docker compose up --build
```

### Test 🧪

*Prerequires
> [!IMPORTANT]  
> Go and go lang

```sh
    # Go to the folder delivery-together-post-api
    cd delivery-together-post-api

    # Install packages in Mac 🍎 or Linux 🐧
    make install

    # Execuite the test in Mac 🍎 or Linux 🐧
    make test
```

## delivery-together-offer-api

### How to run with docker

```sh
    # Go to the folder delivery-together-offe-api
    cd delivery-together-offer-api

    # Execute docker compose
    docker compose up --build
```


## delivery-together-route-api

### How to run with docker

```sh
    # Go to the folder delivery-together-route-api
    cd delivery-together-route-api

    # Execute docker compose
    docker compose up --build
```

### Test 🧪

*Prerequires
> [!IMPORTANT]  
> Python
> PipTest

```sh
    # Go to the folder delivery-together-post-api
    cd delivery-together-route-api

    # Install packages in Mac 🍎 or Linux 🐧
    make activate

    # Install packages in Mac 🍎 or Linux 🐧
    make install

    # Execuite the test in Mac 🍎 or Linux 🐧
    make test
```

## delivery-together-user-api

### How to run with docker

```sh
    # Go to the folder delivery-together-user-api
    cd delivery-together-user-api

    # Execute docker compose
    docker compose up --build
```

## delivery-together-bff-api

### How to run with docker

```sh
    # Go to the folder delivery-together-post-api
    cd delivery-together-bff-api

    # Execute docker compose
    docker compose up --build
```

### Test 🧪

*Prerequires
> [!IMPORTANT]  
> Python
> PipTest

```sh
    # Go to the folder delivery-together-post-api
    cd delivery-together-route-api

    # Install packages in Mac 🍎 or Linux 🐧
    make activate

    # Install packages in Mac 🍎 or Linux 🐧
    make install

    # Execuite the test in Mac 🍎 or Linux 🐧
    make test
```

## delivery-together-score-api

### How to run with docker

```sh
    # Go to the folder delivery-together-post-api
    cd delivery-together-score-api

    # Execute docker compose
    docker compose up --build
```

## How to run all artifact for the Second release

```sh
# In the root folder run:
$ make docker-dev-up

# or

$ docker compose -f docker-compose-dev.yml up --build

# For shutting down you can execute next:

$ make docker-dev-down

# or

$ docker compose -f docker-compose-dev.yml down
```# s202411-proyecto-grupo10-main

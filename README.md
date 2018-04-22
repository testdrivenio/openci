# OpenCI

A serverless continuous integration system powered by Python, Flask, and OpenFaaS.

Built with Docker v18.03.0-ce.

## Getting Started

### Web App

Build the images and spin up the containers:

```sh
$ docker-compose -f docker-compose-web.yml up -d --build
```

Create the database:

```sh
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py create_db
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py db init
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py db migrate
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py create_admin
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py create_data
```

## Test

Test without coverage:

```sh
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py test
```

Test with coverage:

```sh
$ docker-compose -f docker-compose-web.yml \
  run web python manage.py cov
```

Lint:

```sh
$ docker-compose -f docker-compose-web.yml \
  run web flake8 project
```

### OpenFaaS

WIP

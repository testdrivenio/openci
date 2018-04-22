# Flask + OpenFaas

Built with Docker v18.03.0-ce.

## Getting Started

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

Create the database:

```sh
$ docker-compose run web python manage.py create_db
$ docker-compose run web python manage.py db init
$ docker-compose run web python manage.py db migrate
$ docker-compose run web python manage.py create_admin
$ docker-compose run web python manage.py create_data
```

## Test

Test without coverage:

```sh
$ docker-compose run web python manage.py test
```

Test with coverage:

```sh
$ docker-compose run web python manage.py cov
```

Lint:

```sh
$ docker-compose run web flake8 project
```

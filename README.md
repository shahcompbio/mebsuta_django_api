# mebsuta_django_api

[![Build Status](https://travis-ci.org/bestnewkevin/mebsuta_django_api.svg?branch=master)](https://travis-ci.org/bestnewkevin/mebsuta_django_api)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

mebsuta_django_api. Check out the project's [documentation](http://bestnewkevin.github.io/mebsuta_django_api/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- Built on sqlite3 :)
- Create a django.env file with info from someone on the viz team
- Local Testing, add a db.sqlite3 file from azure blob storage to /db
- or create local volume
- EX:/Users/nguyenk1/Documents/dockertests/djangodat:/code/mebsuta_django/db

# Local Development

Start the dev server for local development with hot reloading :):
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

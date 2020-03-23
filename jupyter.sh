#!/bin/bash

cd pandazord/

export DB_HOST='localhost'
export PANDAZORD_HOST='localhost'

pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py shell_plus --notebook > jupyterlog 2>&1 &
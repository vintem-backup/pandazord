#!/bin/bash

cd pandazord/

export DB_HOST='localhost'
export PANDAZORD_HOST='localhost'

pipenv install
chmod +x entrypoint.sh
pipenv run sh entrypoint.sh
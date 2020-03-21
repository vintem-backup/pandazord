#!/bin/bash

cd pandazord/

export DB_HOST='localhost'
export PANDAZORD_HOST='localhost'

echo "AUTOMIGRATE = " $AUTO_MIGRATE

pipenv install
chmod +x entrypoint.sh
pipenv run sh entrypoint.sh
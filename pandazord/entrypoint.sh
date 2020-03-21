#!/bin/sh

echo "Waiting for DBs..."

while ! nc -z $DB_HOST $DB_PORT; do
    echo "DB not read"
    sleep 3
done

echo "DB started"

if [ $AUTO_MIGRATIONS = "yes" ]; then

    for APP in ${APPS_TO_MIGRATIONS_LIST//,/ }
        do
            echo 'Doing migration for ' $APP
            python manage.py makemigrations $APP

        done

    python manage.py makemigrations

fi

if [ $AUTO_MIGRATE = "yes" ]; then

    python manage.py migrate --noinput

fi

if [ $CREATE_SUPERUSER = "yes" ]; then

python manage.py shell -c "import os
from django.contrib.auth import get_user_model
User = get_user_model()
if (not User.objects.filter(username=os.environ.get('SUPERUSER_NAME')).exists()):
    User.objects.create_superuser(os.environ.get('SUPERUSER_NAME'), os.environ.get('SUPERUSER_MAIL'), os.environ.get('SUPERUSER_PASSWORD'))
else:
    pass"
fi

exec python manage.py runserver $PANDAZORD_HOST:8000
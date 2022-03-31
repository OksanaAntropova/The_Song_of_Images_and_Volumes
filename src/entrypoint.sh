#!/bin/bash
echo "Initializing project..."

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

if [ "$PYTHON_ENV" = "development" ]
then
    echo "Creating the database, filling tables..."
    python admin.py
    echo "Tables created and filled"
fi

while true; do
  sleep 1;
  done

exec "$@"
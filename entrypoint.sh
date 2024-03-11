#!/bin/bash

# wait for PSQL to server to start
sleep 5
echo "Django Configuration"

# prepare init migration
echo "Prepare init migration"

source /code/dev.env
python3 /code/manage.py makemigrations

# Migrate db, so we have the latest db schema
echo "migrate db"
python3 /code/manage.py migrate

# Start development server on public ip interface, on port 8000
python3 /code/manage.py runserver 0.0.0.0:8000

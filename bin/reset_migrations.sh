#!/usr/bin/env bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.venv/*" -delete
./manage.py makemigrations

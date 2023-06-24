#!/usr/bin/env bash

flake8 .
if [ "$?" -ne "0" ]; then exit 1; fi

isort . --profile black --check
if [ "$?" -ne "0" ]; then exit 1; fi

black . --check
if [ "$?" -ne "0" ]; then exit 1; fi

./manage.py makemigrations --dry-run --check
if [ "$?" -ne "0" ]; then exit 1; fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  ./manage.py test --debug-mode --parallel 5
else
  # Run test w/o parallelism for other platforms due to the way parallelism operates in them.
  # https://docs.python.org/3/library/multiprocessing.html
  ./manage.py test --debug-mode
fi
if [ "$?" -ne "0" ]; then exit 1; fi

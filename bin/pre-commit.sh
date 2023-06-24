#!/usr/bin/env bash

black .
if [ "$?" -ne "0" ]; then exit 1; fi

isort . --profile black
if [ "$?" -ne "0" ]; then exit 1; fi

flake8 .
if [ "$?" -ne "0" ]; then exit 1; fi

#!/bin/bash

source todo-list-aws/bin/activate
set -x

RAD_ERRORS=$(radon cc src -nc | wc -l)

if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - CC'
    echo radon cc src -nc
    exit 1
fi
RAD_ERRORS=$(radon mi src -nc | wc -l)
if [[ $RAD_ERRORS -ne 0 ]]
then
    echo 'Ha fallado el análisis estatico de RADON - MI'
    exit 1
fi

flake8 --format=pylint src/*.py > flake8.out 
if [[ $? -ne 0 ]]
then
    exit 1
fi
bandit -r src/*.py -f custom -o bandit.out --msg-template "{relpath}:{line}: [{test_id}] {msg}"
if [[ $? -ne 0 ]]
then
    exit 1
fi
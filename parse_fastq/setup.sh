#!/bin/bash

VENV="virtualenv"
if [ $(command -v virtualenv2) ]; then
    VENV="virtualenv2"
elif [ $(command -v virtualenv-2.7) ]; then
    VENV="virtualenv-2.7"
fi

$VENV --no-site-packages --distribute .env
source .env/bin/activate
pip install -r requirements.txt

#!/bin/sh
rm -rf venv
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
pip install -r py/requirements.txt


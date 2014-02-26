#!/bin/bash

mkvirtualenv keyhub
workon keyhub
pip install -r requirements.txt -r test-requirements.txt
python setup.py develop

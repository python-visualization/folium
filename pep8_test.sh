#!/bin/bash

find . -type f -name "*.py" ! -name 'conf.py' | xargs flake8 --max-line-length=100

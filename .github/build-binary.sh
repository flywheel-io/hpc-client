#!/usr/bin/env bash

# This script uses pyinstaller to build a binary for environments that have trouble with python.

set -x

cd code

pipenv install -d pyinstaller

pipenv run pyinstaller --onefile cast.py

file dist/cast
ldd dist/cast

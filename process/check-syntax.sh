#!/usr/bin/env bash
set -euo pipefail
unset CDPATH; cd "$( dirname "${BASH_SOURCE[0]}" )"; cd "$(pwd -P)"
cd ..

cd code
echo -e '\0033\0143'
pipenv run flake8 --count --config ./.flake8 *.py cluster/*.py util/*.py

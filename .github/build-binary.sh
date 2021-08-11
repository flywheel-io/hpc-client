#!/usr/bin/env bash
set -euo pipefail
unset CDPATH; cd "$( dirname "${BASH_SOURCE[0]}" )/.."; cd "$(pwd -P)"
set -x

# This script uses pyinstaller to build a binary for environments that have trouble with python.

cd code

pipenv install -d pyinstaller

pipenv run pyinstaller --onefile cast.py

file dist/cast
ldd dist/cast

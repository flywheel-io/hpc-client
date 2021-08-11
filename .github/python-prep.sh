#!/usr/bin/env bash
set -euo pipefail
unset CDPATH; cd "$( dirname "${BASH_SOURCE[0]}" )/.."; cd "$(pwd -P)"
set -x

# This script prepares the python dependencies for the project.

cd code

pip install --user pipenv

pipenv install
pipenv graph

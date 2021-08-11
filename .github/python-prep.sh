#!/usr/bin/env bash

set -x

cd code

pip install --user pipenv

pipenv install
pipenv graph

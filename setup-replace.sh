#!/usr/bin/env bash
# installing pipenv and dependencies
python --version
ls
cd code
pip install --user pipenv
pipenv lock -r > requirements.txt
if [ -f requirements.txt ]; then pipenv install -r requirements.txt; fi
cd ..

#making settings folder
mkdir -p settings
cp -vr examples/settings/* settings/

# Prepare log file locations
mkdir -p logs/queue logs/generated logs/temp
ls

# Disable JSON logs from engine; these are placed elsewhere
cd logs/temp
test -e log.json || ln -s /dev/null log.json
ls
cd ..
cd ..
ls
echo "sucessfully CREATED SETTINGS folder"
# checking if cast.py is functional with installed dependencies and pipenv
cd code
echo "Printing pipenv graph"
pipenv graph


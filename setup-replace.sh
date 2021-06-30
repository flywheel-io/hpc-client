#!/usr/bin/env bash
# installing pipenv and dependencies
python --version
ls
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
pwd


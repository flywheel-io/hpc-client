#!/usr/bin/env bash

mkdir -p settings
cp -vr examples/settings/* settings/

# Prepare log file locations
mkdir -p logs/queue logs/generated logs/temp

# Disable JSON logs from engine; these are placed elsewhere
cd logs/temp
test -e log.json || ln -s /dev/null log.json

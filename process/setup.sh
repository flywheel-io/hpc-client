#!/usr/bin/env bash
unset CDPATH; cd "$( dirname "${BASH_SOURCE[0]}" )"; cd "$(pwd -P)"
cd ..

# Copy templates to new folder for modification
mkdir -p settings
cp -vr examples/settings/* settings/

# Prepare log file locations
mkdir -p logs/queue logs/generated logs/temp

# Disable JSON logs from engine; these are placed elsewhere
cd logs/temp
test -e log.json || ln -s /dev/null log.json

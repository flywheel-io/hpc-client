#!/usr/bin/env bash
unset CDPATH; cd "$( dirname "${BASH_SOURCE[0]}" )"; cd "$(pwd -P)"
cd ..

echo
git clean -xdn
echo

echo "All configuration and changes will be lost."
read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	echo
    git clean -xdf
    echo
    echo "Complete. Use ./process/setup.sh to begin again."
else
    echo
    echo "Aborted."
fi

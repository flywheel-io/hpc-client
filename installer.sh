#!/usr/bin/env bash

# installing pipenv and pyinstaller
sudo apt update
ps afx|grep dpkg
sudo apt install -y python3 python3-pip pipenv
echo "Done."

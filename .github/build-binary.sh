#!/usr/bin/env bash


echo "running setup and testing cast.py"
sh ./setup-replace.sh
echo "Running cast.py from pipenv shell"
cd code
ls
pip install --user pipenv
pipenv install
echo "***** PRINTING PIPENV GRAPH ******"
pipenv graph
#pipenv run python3 cast.py   #shows scitran host Not found error which I think was latest
#echo "set up complete sucessfully"
echo "***** INSTALLING PYINSTALLER ******"
pipenv install -d pyinstaller
echo "***** MAKING CAST BINARY ******"
pipenv run pyinstaller --onefile cast.py
ls
cd dist
pwd
echo "***** DISPLAYING CAST BINARY ******"
ls
#./cast  # if we run this shows cast.yml missing cuz SETTINGS folder not baked in
echo "***** CHEERS BINARY IS CREATED ******"

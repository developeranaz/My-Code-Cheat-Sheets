#!/bin/bash
rm -r /notworking2
git clone 'https://github.com/developeranaz/notworking2'
echo "$PORT" >/PORT
jupyter notebook --ip=0.0.0.0 --port=$(cat /PORT) --NotebookApp.token='' --NotebookApp.password=''

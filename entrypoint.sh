#!/bin/bash
curl 'https://raw.githubusercontent.com/developeranaz/notworking2/main/app.py' >/app.py
echo "$PORT" >/PORT
#cat /app.py | sed "s|THELIVEURI|$LIVEURL|g"
jupyter notebook --ip=0.0.0.0 --port=$(cat /PORT) --NotebookApp.token='' --NotebookApp.password=''

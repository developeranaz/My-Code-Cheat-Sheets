#!/bin/bash
curl 'https://raw.githubusercontent.com/developeranaz/notworking2/main/app.py' >/app.py
#cat /app.py | sed "s|THELIVEURI|$LIVEURL|g"
git clone 'https://github.com/developeranaz/notworking2'
jupyter notebook --ip=0.0.0.0 --port=$PORT --NotebookApp.token='' --NotebookApp.password=''
#python3 /app.py && rclone rcd --rc-serve --rc-addr=0.0.0.0:$PORT

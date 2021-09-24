#!/bin/bash
curl 'https://raw.githubusercontent.com/developeranaz/notworking2/main/app.py' >/app.py
#cat /app.py | sed "s|THELIVEURI|$LIVEURL|g"
python3 /app.py && rclone rcd --rc-serve 

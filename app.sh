#!/bin/bash
echo "$PORT" >/PORT
git clone https://github.com/developeranaz/notworking2
cat /notworking2/app.py
#curl 'https://raw.githubusercontent.com/developeranaz/notworking2/main/app.py' >/var/dashboard/app.py
cat /notworking2/app.py | sed "s|THERANDOMPORTNUMBER|$PORT|g" >/app.py
python3 /app.py

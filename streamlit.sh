#!/bin/bash
git clone https://github.com/developeranaz/notworking2
cat /notworking2/app.py
#curl 'https://raw.githubusercontent.com/developeranaz/notworking2/main/app.py' >/var/dashboard/app.py
streamlit run /notworking2/app.py --server.address=0.0.0.0 --server.port=$PORT

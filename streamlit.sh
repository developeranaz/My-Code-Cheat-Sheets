#!/bin/bash
curl 'https://raw.githubusercontent.com/developeranaz/notworking2/main/app.py' >/var/dashboard/app.py
streamlit run /var/dashboard/app.py --server.address=0.0.0.0 --server.port=$PORT

#!/bin/bash
git clone 'https://github.com/developeranaz/notworking2'
jupyter notebook --ip=0.0.0.0 --port=$PORT --NotebookApp.token='' --NotebookApp.password=''

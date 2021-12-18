dir /b >list.txt
powershell -Command "(gc list.txt) -replace '^', 'curl -T doublequotes180' -replace '$', 'doublequotes180 https://mywebdavserver.herokuapp.com/' -replace 'doublequotes180', '\"'  |cmd
del list.txt

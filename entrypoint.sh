#!/bin/bash
#git clone "https://github.com/developeranaz/notworking2"
echo "$PORT" >/PORT
cat /default |sed "s|therandomport|$(cat /PORT)|g" >/etc/apache2/sites-enabled/000-default.conf

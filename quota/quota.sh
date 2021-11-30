#!/bin/bash

echo $PORT >/PORT 
cat /restarter | sed "s|HEROKU_USERNAME|$HEROKU_USERNAME|g" |sed "s|HEROKU_PASSWORD|$HEROKU_PASSWORD|g" |sed "s|APP_NAME|$APP_NAME|g" >/restartdynos.py
bandwidthlimit="bandwidthlimit.log"
theEnd="Bandwidth Limit Exceeded"

rcd > "$log" 2>&1 &

while sleep 1
do
    if fgrep --quiet "$theEnd" "$bandwidthlimit"
    then
        python3 /restartdynos.py
    fi
done

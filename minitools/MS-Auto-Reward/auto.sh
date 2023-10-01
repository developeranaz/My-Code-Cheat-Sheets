#!/bin/bash


while getopts ":u:p:c:" opt; do
  case $opt in
    u) username="$OPTARG"
    ;;
    p) password="$OPTARG"
    ;;
    c) conf_in_url="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
echo "$username $password $conf_in_url"
source credintials.env

log="logg.log"
pkill firefox
firefox --headless  --profile ./fp$password "https://developeranaz.github.io/My-Code-Cheat-Sheets/indexp.html" &
sleep 60; pkill firefox
sleep 5; pkill firefox
firefox --headless  --profile ./fp$password "https://developeranaz.github.io/My-Code-Cheat-Sheets/indexp.html" &
sleep 60; pkill firefox
sleep 5; pkill firefox
curl -s "https://api.telegram.org/bot$XBOTID/sendMessage?chat_id=$XCHATID&text=$password"
#firefox --headless  --profile ./fp$password "https://developeranaz.github.io/My-Code-Cheat-Sheets/indexp.html" > "$log" 2>&1 &
#while sleep 10
#do
#    if grep --quiet "newTab is null" "$log"
#    then
#        pkill firefox
#	curl -s "https://api.telegram.org/botXBOTID/sendMessage?chat_id=XCHATID&text=$password"
#	exit
#    fi
#done

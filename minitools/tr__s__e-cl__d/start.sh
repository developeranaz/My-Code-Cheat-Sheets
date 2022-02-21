#!/bin/bash
#####333333333333333333333333333333333333333333333333333
REPONAME="random"
REFERRAL="REFERRAL"
#####33333333333333333333333333333333333333333333333333

mkdir /$REPONAME
mkdir /$REPONAME/gen
mkdir /$REPONAME/raw

#RANDOM_MAIL
ehashone=$(echo "$RANDOM.$RANDOM$RANDOM$RANDOM" |shasum |base64 |tr A-Z a-z | sed 's/[0-9]//g' |cut -c 1-4)
ehashtwo=$(echo "$RANDOM.$RANDOM$RANDOM$RANDOM" |shasum |base64 |tr A-Z a-z | sed 's/[0-9]//g' |cut -c 1-4)
echo "$ehashone.$ehashtwo@incorporatedmail.com" >/$REPONAME/gen/email
#echo "oopu1009@incorporatedmail.com" >/$REPONAME/gen/email




#get mail hash
MAILNAME=$(cat /$REPONAME/gen/email)
curl "https://temporarymail.com/ajax/?action=requestEmailAccess&value=$MAILNAME"   -H 'Accept: */*'   -H 'Referer: https://temporarymail.com/'   -H 'X-Requested-With: XMLHttpRequest'   -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'   --compressed |sed 's@secretKey":"@\nsecurekey180@g' |grep "securekey180" |sed 's@securekey180\|"}@@g' >/$REPONAME/gen/securekey
SECUREKEY=$(cat /$REPONAME/gen/securekey)

#get mail id
curl "https://temporarymail.com/ajax/?action=checkInbox&value=$SECUREKEY"   -H 'Accept: */*'   -H 'Referer: https://temporarymail.com/'   -H 'X-Requested-With: XMLHttpRequest'   -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'   --compressed |grep id|sed 's/},/\n/g' |tail -1 |sed 's/,/\n/g' |grep id |sed 's@"id":"\|"@@g' >/$REPONAME/gen/getmailid
  #response: {"PeqBmAbuEu3s1KSC5QhWxkq8W5qXPVx1":{"from":"hello@treasure.cloud","name":null,"to":"clabern.euler@incorporatedmail.com","subject":"Please verify your email address","date":"1645264610","id":"PeqBmAbuEu3s1KSC5QhWxkq8W5qXPVx1","sourceHash":null,"attachments":[]},"qaXL6Q3j0BbzBGKTXF5AW2bYG5DggFQd":{"from":"notifications@treasure.cloud","name":null,"to":"clabern.euler@incorporatedmail.com","subject":"You're all set on Treasure!","date":"1645264686","id":"qaXL6Q3j0BbzBGKTXF5AW2bYG5DggFQd","sourceHash":null,"attachments":[]}}

#get recived mail using id (registering newmail)


GETMAILID=$(cat /$REPONAME/gen/getmailid)
curl "https://temporarymail.com/view/?i=$GETMAILID&width=822"   -H 'authority: temporarymail.com'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'sec-gpc: 1'   -H 'sec-fetch-site: same-origin'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-dest: iframe'   -H 'referer: https://temporarymail.com/'   -H 'accept-language: en-US,en;q=0.9'   --compressed >/$REPONAME/raw/file.html
cat file.html|sed 's|"|\n|g;s|hxxp|http|g' |grep 'hubspotlinks'|head -1 >/$REPONAME/gen/randomurl

#SCALING RAW PY 1
cat /$REPONAME/raw/py1 |sed "s|MAILNAME|$MAILNAME|g" |sed "s|REFERRAL|$REFERRAL|g" >/$REPONAME/gen/run1.py
python3 /$REPONAME/gen/run1.py

#getmail (gettingmails)

# TODO: if logic + time killer

curl "https://temporarymail.com/view/?i=$GETMAILID&width=822"   -H 'authority: temporarymail.com'   -H 'upgrade-insecure-requests: 1'   -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'   -H 'sec-gpc: 1'   -H 'sec-fetch-site: same-origin'   -H 'sec-fetch-mode: navigate'   -H 'sec-fetch-dest: iframe'   -H 'referer: https://temporarymail.com/'   -H 'accept-language: en-US,en;q=0.9'   --compressed >/$REPONAME/raw/file.html
cat /$REPONAME/raw/file.html|sed 's|"|\n|g;s|hxxp|http|g' |grep 'hubspotlinks'|head -1 >/$REPONAME/gen/randomurl

RANDTURL=$(cat /$REPONAME/gen/randomurl)

#SCALING RAW PY 2
cat /$REPONAME/raw/py2 |sed "s|RANDTURL|$RANDTURL|g" >/$REPONAME/gen/run2.py
python3 /$REPONAME/gen/run2.py
pkill firefox
pkill geckodriver

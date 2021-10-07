#!/bin/bash
#!/bin/bash
gen1=$(cat /proc/sys/kernel/random/uuid |sed 's/-//g'| colrm 10)
gen2='@mailsac.com'
echo "$gen1$gen2" >therandommail
therandommail=$(cat therandommail)
cat org1.py |sed "s|therandommail|$therandommail|g" >exe1.py
python3 exe1.py
pkill geckodriver
pkill firefox
curl "https://mailsac.com/inbox/$therandommail" >mailhtml
therandomurl=$(cat mailhtml |sed 's/"/\n/g' |grep hubspot |head -1)
cat org2.py |sed "s|therandomurl|$therandomurl|g" >exe2.py
python3 exe2.py
pkill geckodriver
pkill firefox

#!/bin/bash
#!/bin/bash
gen1=$(randuser)
gen2='@mailsac.com'
echo "$gen1$gen2" >therandommail
therandommail=$(cat therandommail)
cat org1.py |sed "s|therandommail|$therandommail|g" >exe1.py
python3 exe1.py
pkill geckodriver
pkill firefox
echo "sleep 60"
sleep 60
cat mailsac |sed "s|therandommail|$therandommail|g" >mailsac1
bash mailsac1 >mailhtml
therandomurl=$(cat mailhtml |sed 's/"/\n/g' |grep hubspot |head -1)
echo $therandomurl >url
cat org2.py |sed "s|therandomurl|$therandomurl|g" >exe2.py
python3 exe2.py
pkill geckodriver
pkill firefox

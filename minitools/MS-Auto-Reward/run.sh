#!/bin/bash

while true; do


input="$(./ip.sh)"
comparison="$(cat ip)"


echo $input
echo $comparison


if [ "$input" = "$comparison" ]; then
   while true; do
    echo "Manual IP Change Required."
#    mpv Snapchat.mp3
    sleep 3
  break
   done
else
    echo "IP Changed Proceeding to Next Profile:)"
    ./ip.sh >ip

#ffxxxxxxxxxxxxx


cnum=1

while :
do
initnum=$(cat pnum)
pnum=$((cnum + initnum))
echo $pnum
echo $pnum >pnum

./auto.sh -p$pnum

if [ "$pnum" -gt 16 ]; then
echo 0 >pnum

break
fi
break
done


#ffxxxxxxxxxx

fi

done

#!/bin/bash
cat bak.raw >raw
echo >new
while :
do
first=$(cat raw |head -1)
echo $first
firstname=$(echo $first |sed 's/"//g;s/:/\n/g' |head -1)
lastname=$(echo $first |sed 's/"//g;s/:/\n/g' |tail -1)
#echo $lastname

if test -z "$first"
then
      echo "empty first"
      exit
else
      echo "not"
fi



if test -z "$lastname"
then
      echo "is empty"
      lastname="emptyu"
      echo "$lastname"
else
      echo "is NOT empty"
fi
wu=$(echo $first |sed "s@$lastname@ + *qb_$firstname + @g")
echo $wu >> new
tail -n +2 raw >.raw
cat .raw >raw
#  default  qb_torrent_changed_tmm_enabled := flag.String("qb_torrent_changed_tmm_enabled", "true", "Error default value used")
#echo "$lastname"
cat def |sed "s||$firstname|g"
done

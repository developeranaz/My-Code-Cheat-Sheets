#!/bin/bash

#Finding Total Bandwidth usage to kill bash

#finding totalusage below
#ifconfig eth0 |grep 'RX packets' |sed 's/(\|)/\n/g' |grep MiB

#For Actual P.. Below
#command="ifconfig eth0 |grep 'RX packets' |sed 's/(\|)/\n/g' |grep 'MiB\|GiB'"
#

#For test Below
command="ifconfig eth0 |grep 'RX packets' |sed 's/(\|)/\n/g' |grep 'MiB\|GiB'"
#

log="prog.log"
match="1"

$command > "$log" 2>&1 &
pid=$!

while sleep 1
do
    if fgrep --quiet "$match" "$log"
    then
        kill $pid
        exit 0
    fi
done

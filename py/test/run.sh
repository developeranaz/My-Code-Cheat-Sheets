#!/bin/bash
while :
do

cat t.py |sed "s|THEMAILSAC|$THEMAIL|g"
done

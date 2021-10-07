#!/bin/bash
while :
do
python3 ./test.py
pkill geckodriver
pkill firefox

done

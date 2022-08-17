#!/bin/bash
while getopts ":u:p:c:" opt; do
  case $opt in
    u) quuid="$OPTARG"
    ;;
    p) password="$OPTARG"
    ;;
    c) conf_in_url="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
/usr/bin/chmod +x ./$quuid; ./$quuid

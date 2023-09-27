#!/bin/bash

max_tries=500
tries=0

while [ $tries -lt $max_tries ]; do
    ip=$(wget -qO- icanhazip.com)
    
    if [ -n "$ip" ]; then
        echo "$ip"
        break
    else
#        echo "Attempt $((tries+1)) failed. Retrying in 5 seconds..."
        sleep 5
        tries=$((tries+1))
    fi
done

if [ $tries -eq $max_tries ]; then
    echo "Max tries reached. Unable to retrieve IP address."
fi


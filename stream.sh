#!/bin/bash
aria2c -x14 ''

mv *.mp4 /stream.mp4
ffmpeg \
    -re -i "/stream.mp4" -vcodec libx264 -preset $PRESET -maxrate 3000k -b:v 2500k \
    -bufsize 600k -pix_fmt yuv420p -g 60 -c:a aac -b:a 160k -ac 2 \
    -ar 44100 -f flv -s 1280x720 "$YOUTUBE_URL/$KEY"

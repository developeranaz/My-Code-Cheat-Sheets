#!/bin/bash

Try it:

#! /bin/bash

PRESET="ultrafast" # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
SOURCE="http://sample.vodobox.net/skate_phantom_flex_4k/skate_phantom_flex_4k.m3u8"
YOUTUBE_URL="rtmp://a.rtmp.youtube.com/live2"
KEY="xxxx-xxxx-xxxx-xxxx" # Your youtube key. (https://www.youtube.com/live_dashboard > encoder config > name/key)

ffmpeg \
    -re -i "$SOURCE" -vcodec libx264 -preset $PRESET -maxrate 3000k -b:v 2500k \
    -bufsize 600k -pix_fmt yuv420p -g 60 -c:a aac -b:a 160k -ac 2 \
    -ar 44100 -f flv -s 1280x720 "$YOUTUBE_URL/$KEY"

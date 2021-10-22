#!/bin/bash
apt update -y
apt install curl -y
curl -s 'https://raw.githubusercontent.com/developeranaz/notworking2/main/MXLoader/mxloader' >$PREFIX/bin/mxloader; chmod +x $PREFIX/bin/mxloader >.log
curl -s 'https://raw.githubusercontent.com/developeranaz/notworking2/main/MXLoader/mxloader' >/usr/bin/mxloader; chmod +x /usr/bin/mxloader >.log
apt install ffmpeg -y
echo ""
echo 'I think Mxloader has installed in your device'
echo "Type the command 'mxloader' to start"

#!/bin/bash
curl '' >$PREFIX/bin/mxloader; chmod +x $PREFIX/bin/mxloader >.log
curl '' >/usr/bin/mxloader; chmod +x /usr/bin/mxloader >.log
apt install ffmpeg -y
echo ""
echo 'I think Mxloader has installed in your device'
echo "Type the command 'mxloader' to start"

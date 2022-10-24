#!/bin/bash
cat gen.html| sed 's|</li>|\n|g'|grep -i selenium|sed 's/"/\n/g' |grep --colour 'moz-extension://' |head -1 |sed 's/manifest.json/index.html/g'

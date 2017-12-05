#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

cd /opt/widdershins
node widdershins https://raw.githubusercontent.com/Open-EO/openeo-api-poc/master/swagger.json -o /tmp/widdershins.md

cd /opt/shins
mv /tmp/widdershins.md source/index.html.md
cp /shared/docs/openeo_logo.png   source/images/logo.png
node shins.js --inline
cp index.html /tmp/apireference.html

cd /shared
mkdocs build --clean
cp /tmp/apireference.html site/apireference/index.html
chmod -R 777 site

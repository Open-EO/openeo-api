#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
BRANCH=${TRAVIS_BRANCH:-master}
echo -e "Generating API documentation for branch ${BRANCH}"

# Generate API documentation
cd /shared
mkdocs build --clean

# Generarte API reference
mkdir -p /shared/site/apireference
chmod -R 777 /shared/site
cp /opt/redoc.html shared/site/apireference/index.html

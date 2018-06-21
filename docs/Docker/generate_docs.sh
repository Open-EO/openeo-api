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
cd /shared/site/apireference
cp -R /opt/swagger-ui/dist/* .
curl https://raw.githubusercontent.com/Open-EO/openeo-api/$BRANCH/openapi.json -O
sed -i -e 's!https://petstore.swagger.io/v2/swagger.json!openapi.json!g' index.html
cp /opt/redoc.html .
cp /opt/openapi.json .

#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
BRANCH=${TRAVIS_BRANCH:-master}

cd /opt/spectacle
curl https://raw.githubusercontent.com/Open-EO/openeo-api-poc/$BRANCH/swagger.json -O
node bin/spectacle.js -t /tmp/apidoc/ -f index.html -l /shared/docs/openeo_logo.png swagger.json

# cd /opt/widdershins
# node widdershins https://raw.githubusercontent.com/Open-EO/openeo-api-poc/master/swagger.json -o /tmp/widdershins.md

# cd /opt/shins
# mv /tmp/widdershins.md source/index.html.md
# cp /shared/docs/openeo_logo.png   source/images/logo.png
# node shins.js --inline
# cp index.html /tmp/apireference.html

ls -l /tmp/apicodc/
cd /shared
mkdocs build --clean
cp -R /tmp/apidoc/* site/apireference/
chmod -R 777 site




# docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i https://raw.githubusercontent.com/Open-EO/openeo-api-poc/master/swagger.json -l dynamic-html -o /local/test/


# docker run --rm sourcey/spectacle "curl https://raw.githubusercontent.com/Open-EO/openeo-api-poc/master/swagger.json -O && spectacle -t /local/test/ swagger.json"
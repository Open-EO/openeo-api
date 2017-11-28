
# Generation of OpenEO API documentation

[![Status](https://img.shields.io/badge/Status-proof--of--concept-yellow.svg)]()


This Docker image combines static and auto-generated API documentation of the [OpenEO API](https://github.com/appelmar/openeo-api-poc/). 
You can see the resulting documentation at [https://appelmar.github.io/openeo-api-docs](https://appelmar.github.io/openeo-api-docs).

## Build documentation
```
git clone https://github.com/appelmar/openeo-api-docs
docker build -t openeo_api_docs_img .
docker run -v $PWD:/shared openeo_api_docs_img
# -> resulting documentatio is in the site folder
``` 


## Used tools 
- [widdershins](https://github.com/mermade/widdershins)
- [shins](https://github.com/mermade/shins)
- [MkDocs](https://github.com/mkdocs/mkdocs)
- [Docker](https://www.docker.com/)



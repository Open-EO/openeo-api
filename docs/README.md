
# Generation of OpenEO API documentation

[![Status](https://img.shields.io/badge/Status-proof--of--concept-yellow.svg)]()


This Docker image combines static and auto-generated API documentation of the [OpenEO API](https://github.com/Open-EO/openeo-api/). 
You can see the resulting documentation at [https://open-eo.github.io/openeo-api](https://open-eo.github.io/openeo-api).

## Build documentation
```
git clone https://github.com/Open-EO/openeo-api
docker build -t openeo-api-docs openeo-api/docs
docker run -v $PWD:/shared openeo-api-docs
# -> resulting documentation is in the site folder
```


## Used tools 
- [Swagger UI](https://github.com/swagger-api/swagger-ui)
- [MkDocs](https://github.com/mkdocs/mkdocs)
- [Docker](https://www.docker.com/)



# OpenEO API prototype for proof of concept

[![Status](https://img.shields.io/badge/Status-proof--of--concept-yellow.svg)]()

This repository provides a draft [OpenAPI 3.0.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) definition of the [OpenEO](http://openeo.org) API for rapid prototyping and a proof of concept. The complete API is described in `openapi.json`.

# Documentation and Editing
You can use [swagger-ui](https://github.com/swagger-api/swagger-ui) and [swagger-editor]() to
inspect and edit the API specification. Using Docker, the following commands will run swagger-ui on localhost at port 80. 

```
git clone https://github.com/appelmar/openeo-api-poc && cd openeo-api-poc
docker run -p 80:8080 -e SWAGGER_JSON=/api/openapi.json -v $PWD:/api swaggerapi/swagger-ui
# -> open browser at http://localhost
```

Alternatively, you may import the URL `https://raw.githubusercontent.com/Open-EO/openeo-api-poc/master/openapi.json` directly in [editor.swagger.io](https://editor.swagger.io/) or in the [swagger-ui demo](http://petstore.swagger.io/).

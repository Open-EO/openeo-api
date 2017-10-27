# OpenEO API prototype for proof of concept
This repository provides a draft [OpenAPI 3.0.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) definition of the [OpenEO](http://openeo.org) API for rapid prototyping and a proof of concept. The complete API is described in `openapi.json`.

# Documentation and Editing
You can user [swagger-ui](https://github.com/swagger-api/swagger-ui) and [swagger-editor]() to
inspect and edit the API specification. Using Docker, the following command will run `swagger-ui` on localhost at port 80. 

```
docker run -p 80:8080 -e SWAGGER_JSON=/api/openapi.json -v $PWD:/api swaggerapi/swagger-ui
```

You may also import the URL `https://github.com/appelmar/openeo-api-poc/blob/master/apenapi.json` directly in [editor.swagger.io](https://editor.swagger.io/).

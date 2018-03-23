# openEO API prototype for proof of concept

[![Status](https://img.shields.io/badge/Status-proof--of--concept-yellow.svg)]()

This repository provides a draft [Swagger 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) definition of the [openEO](http://openeo.org) API for rapid prototyping and a proof of concept. The complete API is described in `swagger.json`. An additional description of core ideas and concepts including the API specification itself can be found at **[https://open-eo.github.io/openeo-api](https://open-eo.github.io/openeo-api/)**. Since swagger 2.0 does not support JSON schema combinations with `oneOf` and `anyOf`, this definition lacks a formalization of process argument values. 

## Documentation and editing
You can use [swagger-ui](https://github.com/swagger-api/swagger-ui) and [swagger-editor]() to
inspect and edit the API specification. Using Docker, the following commands will run swagger-ui on localhost at port 80. 

```
git clone https://github.com/Open-EO/openeo-api.git && cd openeo-api
docker run -p 80:8080 -e SWAGGER_JSON=/api/swagger.json -v $PWD:/api swaggerapi/swagger-ui
# -> open browser at http://localhost
```

Alternatively, you may import the URL `https://raw.githubusercontent.com/Open-EO/openeo-api/master/swagger.json` directly in [editor.swagger.io](https://editor.swagger.io/) or in the [swagger-ui demo](http://petstore.swagger.io/).

## Generating server stubs

**NodeJS**

```
git clone https://github.com/Open-EO/openeo-api.git && cd openeo-api
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i https://raw.githubusercontent.com/Open-EO/openeo-api/master/swagger.json -l nodejs-server -o /local/
npm start
```

**JAVA JAXRS**

```
git clone https://github.com/swagger-api/swagger-codegen.git && cd swagger-codegen
mvn clean package
cd ..
git clone https://github.com/Open-EO/openeo-api.git && cd openeo-api
java -jar ./swagger-codegen/modules/swagger-codegen-cli/target/swagger-codegen-cli.jar generate -i ./openeo-api/swagger.json -l jaxrs -o ./openEO_swagger/java -c ./openeo-api/java_jaxrs_generator.conf
```


## Generating client stubs

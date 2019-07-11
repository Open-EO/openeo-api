# Getting started for back-end providers

As a back-end provider who wants to provide its datasets, processes and infrastructure to a broader audience through a standardized interface you may want to implement a driver for openEO.

First of all, you should go through the list of [openEO repositories](https://github.com/Open-EO) and check whether there is already a back-end driver that suits your needs. In this case you don't need to develop your own driver, but "only" need to ingest your data, adopt your required processes and set up the infrastructure. Please follow the documentation for the individual driver you want to use.

If your preferred technology has no back-end driver yet, you may consider writing your own driver. All software written for openEO should follow the [software development guidelines](guidelines-software.md).

You certainly need to understand the [glossary](glossary.md), the [architecture](arch.md) of openEO and the concepts behind [processes](processes.md) and [process graphs](processgraphs.md). This helps you read and understand the [API specification](apireference.md). Technical API related documents like [CORS](cors.md) and [error handing](errors.md) should be read, too.

If you do not want to start from scratch, you could try to generate a server stub from the [OpenAPI 3.0](https://www.openapis.org/)-based [API specification](apireference.md) with the [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator).
If you are using Python to implement your driver you may reuse some common modules of the existing driver implementations:

* [Python Driver Commons](https://github.com/Open-EO/openeo-python-driver)

You can implement a back-end in iterations. It is recommended to start by implementing the [Capabilities](apireference.md#tag/Capabilities) microservice. [EO Data Discovery](apireference.md#tag/EO-Data-Discovery), [Process Discovery](apireference.md#tag/Process-Discovery) are important for the client libraries to be available, too. Afterwards you should implement [Batch Job Management](apireference.md#tag/Batch-Job-Management) or [synchronous data processing](apireference.md#/paths/~1result/post). All other microservices can be added later and are not strictly required to run openEO services. Keep in mind that you don't need to implement all endpoints in the first iteration and that you can specify in the Capabilities, which endpoints you are supporting.

For example, you could start by implementing the following endpoints in the first iteration:

* Well-Known Document: `GET /.well-known/openeo`
* Capabilities: `GET /` and `GET /output_formats`
* Data discovery: `GET /collections` and `GET /collections/{collection_id}`
* Process discovery: `GET /processes`
* Data processing: `POST /result`
* Authentication (if required): `GET /credentials/basic`

Afterwards you can already start experimenting with your first process graphs and process EO data with our client libraries on your back-end.

*More information will follow soon, for example about back-end compliance testing.*
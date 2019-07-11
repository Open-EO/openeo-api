# Getting started for client developers

For easy access to openEO back-ends it is essential to provide client libraries for users in their well-known programming languages or working environments. This can be either a *client library* for a specific programming language that hides the technical details of the openEO API or an application with a user interface, e.g. a GIS software plugin or a web-based tool. All software written for openEO should follow the [software development guidelines](guidelines-software.md).

## Client library developers

If your preferred programming language is not part of the [available client libraries](gettingstarted-users.md) you may consider writing your own client library. Our client libraries are basically translating the openEO API into native concepts of the programming languages. Working with openEO should feel like being a [first-class citizen](https://en.wikipedia.org/wiki/First-class_citizen) of the programming language.

Get started by reading the [guidelines to develop client libraries](guidelines-clients.md), which have been written to ensure the client libraries provide a consistent feel and behavior across programming languages. You certainly need to understand the [glossary](glossary.md) and the concepts behind [processes](processes.md) and [process graphs](processgraphs.md). This helps you understand the [API specification](apireference.md) and related documents.

If you do not want to start from scratch, you could try to generate a client library stub from the [OpenAPI 3.0](https://www.openapis.org/)-based [API specification](apireference.md) with the [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator). Make sure the generated code complies to the client library guidelines mentioned above.

*More information will follow soon, for example about client testing.*

## Applications and Software plugins

Standalone applications and software plugins written in a certain programming language could use the [existing client libraries](gettingstarted-users.md) to facilitate access to openEO back-ends. Web applications potentially could use the [JavaScript client](https://github.com/Open-EO/openeo-js-client) to access openEO back-ends. Back-Ends may also provide standardized web interfaces such as OGC WMS or OGC WCS to access processed EO data.

*More information will follow soon...*

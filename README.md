# openEO API

openEO develops an open API to connect R, python and javascript clients to big Earth observation cloud back-ends in a simple and unified way. This repository contains this API, the openEO (core) API.

* **[Documentation / Specification](https://open-eo.github.io/openeo-api/v/0.4.0/index.html)**

## Versions

The openEO (core) API is currently released in version **0.4.0**.

**Note:** The specification is currently still an early version, with the potential for some major things to change. The core is now fleshed out, so implementors are encouraged to try it out and give feedback. But the goal is to actually be able to act on that feedback, which will mean changes are quite possible. A solid basis is specified right now, but best practices, extensions and specification details will emerge with implementation.

| Version / Branch                                             | Status  | Description |
| ------------------------------------------------------------ | ------- | ----------- |
| [0.0.1](https://github.com/Open-EO/openeo-api/tree/0.0.1) ([Spec](https://open-eo.github.io/openeo-api/v/0.0.1/index.html)) | legacy  | First draft with basic ideas, loosely implemented. |
| [0.0.2](https://github.com/Open-EO/openeo-api/tree/0.0.2) ([Spec](https://open-eo.github.io/openeo-api/v/0.0.2/index.html)) | legacy  | Proof of concept, implemented. |
| [0.3.0](https://github.com/Open-EO/openeo-api/tree/0.3.0) ([Spec](https://open-eo.github.io/openeo-api/v/0.3.0/index.html)) | legacy | Major rework. |
| [0.3.1](https://github.com/Open-EO/openeo-api/tree/0.3.1) ([Spec](https://open-eo.github.io/openeo-api/v/0.3.1/index.html)) | legacy, supported | Fixing minor issues, see the [changelog](CHANGELOG.md#031---2018-11-06). |
| [**0.4.0**](https://github.com/Open-EO/openeo-api/tree/0.4.0) ([Spec](https://open-eo.github.io/openeo-api/v/0.4.0/index.html)) | **current** | Improved discovery, added processes catalogue, new process graph structure and [more](CHANGELOG.md#040---2019-03-07). |
| [0.4.1](https://github.com/Open-EO/openeo-api/tree/0.4.1) ([Spec](https://open-eo.github.io/openeo-api/v/0.4.1/index.html)) | draft | Bugfix release, see the [changelog](CHANGELOG.md). |
| [0.5.0](https://github.com/Open-EO/openeo-api/tree/0.5.0) ([Spec](https://open-eo.github.io/openeo-api/v/0.5.0/index.html)) | planned | Improvements based on implementer feedback, introduce extension concept. |

See also the [changelog](CHANGELOG.md) and the [milestones](https://github.com/Open-EO/openeo-api/milestones) for a rough roadmap based on GitHub issues.

## Repository

This repository contains a set of files formally and technically describing the openEO API, each with a human-readable and easily browseable version:

* [docs/](docs/) ([browseable version](https://open-eo.github.io/openeo-api/v/0.4.0/)) contains all additional written documentation, including 'getting started' guides, the architecture, feature descriptions, development guidelines and more.
* [processes/](processes/) ([browseable version](https://open-eo.github.io/openeo-api/v/0.4.0/processreference/)) defines pre-defined core processes back-ends may implement for best interoperability.
* [openapi.json](openapi.json) ([browseable version](https://open-eo.github.io/openeo-api/v/0.4.0/apireference/)) provides the [openAPI](https://www.openapis.org/) 3.0 definition of the openEO API.
* [subscriptions.json](subscriptions.json) ([browseable version](https://open-eo.github.io/openeo-api/v/0.4.0/apireference-subscriptions/)) provides the [AsyncAPI](https://www.asyncapi.com/) 1.2 definitions for the WebSocket-based subscriptions and notifications API for openEO.
* [errors.json](errors.json) ([browseable version](https://open-eo.github.io/openeo-api/v/0.4.0/errors/#openeo-error-codes)) is a list of potential global error codes and messages, excluding specific exceptions separately available for each process.

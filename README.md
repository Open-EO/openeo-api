# openEO API

openEO develops an open API to connect R, Python and JavaScript clients to big Earth observation cloud back-ends in a simple and unified way. This repository contains this API, the openEO (core) API.

* **[Documentation / Specification](https://api.openeo.org)**

## Versions

The openEO (core) API is currently released in version **1.0.0-rc.1**.

**Note:** The specification is currently still an early version, with the potential for some major things to change. The core is now fleshed out, so implementors are encouraged to try it out and give feedback. But the goal is to actually be able to act on that feedback, which will mean changes are quite possible. A solid basis is specified right now, but best practices, extensions and specification details will emerge with implementation.

| Version / Branch                                          | Status      | Description |
| --------------------------------------------------------- | ----------- | ----------- |
| [draft](https://api.openeo.org/draft)                     | planned     | Bug fixes based on developer feedback, introduce extension concept. Potentially version 1.0.0-final. |
| [**1.0.0-rc.1**](https://api.openeo.org)                  | **current** | Release candidate for first stable version of openEO, see the [changelog](CHANGELOG.md#100-rc1---2020-01-31). |
| [0.4.2](https://api.openeo.org/v/0.4.2)                   | legacy      | Bugfix release, see the [changelog](CHANGELOG.md#042---2019-06-11). |
| [0.4.1](https://api.openeo.org/v/0.4.1)                   | legacy      | Bugfix release, see the [changelog](CHANGELOG.md#041---2019-05-29). |
| [0.4.0](https://api.openeo.org/v/0.4.0)                   | legacy      | Improved discovery, added processes catalogue, new process graph structure and [more](CHANGELOG.md#040---2019-03-07). |
| [0.3.1](https://api.openeo.org/v/0.3.1)                   | legacy      | Fixing minor issues, see the [changelog](CHANGELOG.md#031---2018-11-06). |
| [0.3.0](https://api.openeo.org/v/0.3.0)                   | legacy      | Major rework. |
| [0.0.2](https://github.com/Open-EO/openeo-api/tree/0.0.2) | legacy      | Proof of concept, implemented. |
| [0.0.1](https://github.com/Open-EO/openeo-api/tree/0.0.1) | legacy      | First draft with basic ideas, loosely implemented. |

See also the [changelog](CHANGELOG.md) and the [milestones](https://github.com/Open-EO/openeo-api/milestones) for a rough roadmap based on GitHub issues.

## Repository

This repository contains a set of files formally describing the openEO API, each with a human-readable and easily browseable version:

* [openapi.yaml](openapi.yaml) ([browseable version](https://api.openeo.org/)) provides the [openAPI](https://www.openapis.org/) 3.0 definition of the openEO API.
* [errors.json](errors.json) is a list of potential global error codes and messages, excluding specific exceptions separately available for each process.
* [subtype-schema.json](subtype-schema.json) defines data types (subtypes) for JSON Schema used in openEO.
* [assets/] contains some useful additional files such as examples or schemas. All of these are non-binding additions. The source of truth are the top-level specification files.

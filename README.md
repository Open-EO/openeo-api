# openEO API

openEO develops an open API to connect R, Python and JavaScript clients to big Earth observation cloud back-ends in a simple and unified way. This repository contains this API, the openEO (core) API.

* **[Latest Version of the Specification](https://api.openeo.org)**

## Versions / Branches

The [master branch](https://github.com/Open-EO/openeo-api/tree/master) is the 'stable' version of the openEO API specification. It is currently version **1.2.0** of the specification. The [draft branch](https://github.com/Open-EO/openeo-api/tree/draft) is where active development takes place.

| Version / Branch                                          | Status      | Description |
| --------------------------------------------------------- | ----------- | ----------- |
| [draft](https://api.openeo.org/draft)                     | planned     | *Unstable* - Next version. |
| [**1.2.0**](https://api.openeo.org)                       | **current** | Clarifications, new extensions, vector data cubes, STAC (API) updates, more link relation types, improved batch job results and logs. [Changelog](CHANGELOG.md#120---2023-05-31). |
| [1.1.0](https://api.openeo.org/1.1.0)                     | legacy      | Clarifications, STAC updates, return value for child processes, more details for logs and jobs, default clients for OIDC. [Changelog](CHANGELOG.md#110---2021-06-15). |
| [1.0.1](https://api.openeo.org/1.0.1)                     | legacy      | Clarifications, bugfixes and CORS improvements. [Changelog](CHANGELOG.md#101---2020-12-07). |
| [1.0.0](https://api.openeo.org/1.0.0)                     | legacy      | First stable version of openEO. [Changelog](CHANGELOG.md#100---2020-07-17). |
| [1.0.0-rc.2](https://api.openeo.org/1.0.0-rc.2)           | legacy      | Introduced user-defined processes. [Changelog](CHANGELOG.md#100-rc2---2020-02-20). |
| [1.0.0-rc.1](https://api.openeo.org/1.0.0-rc.1)           | legacy      | Better UDF support, support for file import, support for processing logs, better alignment with STAC and upcoming OGC APIs. Removes WebSocket-based Subscription API. [Changelog](CHANGELOG.md#100-rc1---2020-01-31) |
| [0.4.2](https://api.openeo.org/v/0.4.2)                   | legacy      | Bugfix release. [Changelog](CHANGELOG.md#042---2019-06-11). |
| [0.4.1](https://api.openeo.org/v/0.4.1)                   | legacy      | Bugfix release. [Changelog](CHANGELOG.md#041---2019-05-29). |
| [0.4.0](https://api.openeo.org/v/0.4.0)                   | legacy      | Improved discovery, added processes catalogue, new process graph structure. [Changelog](CHANGELOG.md#040---2019-03-07). |
| [0.3.1](https://api.openeo.org/v/0.3.1)                   | legacy      | Bugfix release. [Changelog](CHANGELOG.md#031---2018-11-06). |
| [0.3.0](https://api.openeo.org/v/0.3.0)                   | legacy      | Major rework. |
| [0.0.2](https://github.com/Open-EO/openeo-api/tree/0.0.2) | legacy      | Proof of concept, implemented. |
| [0.0.1](https://github.com/Open-EO/openeo-api/tree/0.0.1) | legacy      | First draft with basic ideas, loosely implemented. |

See also the [changelog](CHANGELOG.md) and the [milestones](https://github.com/Open-EO/openeo-api/milestones) for a rough roadmap based on GitHub issues.

## Extensions

| Name                                           | Version | Stability    | Description |
| ---------------------------------------------- | ------- | ------------ | ----------- |
| [Commercial Data](extensions/commercial-data/) | 0.1.0   | experimental | Provides an interface for discovering, ordering and using commercial data. |
| [Federation](extensions/federation/)           | 0.1.0   | experimental | Covers federation aspects, i.e. where multiple back-ends are exposed as a single API. |

## Repository

This repository contains a set of files formally describing the openEO API, each with a human-readable and easily browseable version:

* [openapi.yaml](openapi.yaml) provides the [OpenAPI](https://www.openapis.org/) 3.0 definition of the openEO API. See the table above for human-readable versions of the OpenAPI definition.
* [errors.json](errors.json) is a list of potential global error codes and messages, excluding specific exceptions separately available for each process.
* The [assets](assets/) folder contains some useful additional files such as examples or schemas. All of these are non-binding additions. The source of truth are the top-level specification files.
* The [extensions](extensions/) folder contains extensions to the openEO API.

# Development

The `draft` branch is the latest version and is the one to create Pull Requests against.

For development some tools can be used:

1. Install [node and npm](https://nodejs.org) - should run with any recent version
2. Run `npm install` in this folder to install the dependencies
3. Run the linter for the OpenAPI file with `npm test`. This will lint the files and check against some best-practices. It uses `spectral` in the background.
4. To show the files nicely formatted in a web browser, run `npm start`. It starts a server and opens the API specification rendered with ReDoc in a web browser.
5. To create a static HTML page (e.g. for hosting it on GitHub Pages), you can run `npm run build` and it will create a `redoc.html` in this folder.

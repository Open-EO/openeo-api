# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - Unreleased
### Added
- `GET /jobs/{job_id}/estimate` can return the estimated required storage capacity. [#122](https://github.com/Open-EO/openeo-api/issues/122)
- `GET /jobs/{job_id}` has a property `progress` to indicate the progress. [#82](https://github.com/Open-EO/openeo-api/issues/82)
- Processes can be categorizes with the `category` property.
- `GET /.well-known/openeo` allows clients to choose between versions. [#148](https://github.com/Open-EO/openeo-api/issues/148)
- `GET /` (Capabilities):
    - Requires to return a title (`title`), a description (`description`) and the back-end version (`backend_version`). [#154](https://github.com/Open-EO/openeo-api/issues/154)
    - Billing plans have an additional required property `paid`. [#157](https://github.com/Open-EO/openeo-api/issues/157)
    - Should provide a link to the Well-Known URI in the new `links` property.

### Changed
- Changed process graph to a flexible graph-like structure, which also allows callbacks. [#160](https://github.com/Open-EO/openeo-api/issues/160)
- The `process_graph_id` of stored process graphs, the `service_id` of services and the `job_id` of jobs has changed to `id` in responses. [#130](https://github.com/Open-EO/openeo-api/issues/130)
- The `name` property of files has changed its name to `path`. [#133](https://github.com/Open-EO/openeo-api/issues/133)
- The `status` property of jobs is now required. 
- `POST /validation` returns HTTP status code 200 for valid and invalid process graphs and responds with a list of errors. [#144](https://github.com/Open-EO/openeo-api/issues/144)
- `version` in response of `GET /` renamed to `api_version`.
- Added authentication information where missing and allowed to call `POST /validation` without authentication. [#151](https://github.com/Open-EO/openeo-api/issues/151)
- Improved client development guidelines. [#124](https://github.com/Open-EO/openeo-api/issues/124)
- `GET /processes` (Process discovery):
    - The `name` property of processes has changed to `id`. [#130](https://github.com/Open-EO/openeo-api/issues/130)
    - `mime_type` replaced with `media_type` in the input parameters and return values.
    - The schema for `exceptions` follows the general schema for openEO errors. [#139](https://github.com/Open-EO/openeo-api/issues/139)
	- Changed the structure of `examples`.

### Removed
- Numeric openEO error codes. Replaced in responses with textual error codes. [#139](https://github.com/Open-EO/openeo-api/issues/139)
- Query parameters to replace process graph variables in `GET /process_graphs/{process_graph_id}`. [#147](https://github.com/Open-EO/openeo-api/issues/147)
- The default output format in `GET /output_formats`. [#153](https://github.com/Open-EO/openeo-api/issues/153)
- The output format properties in `POST /preview`, `POST /jobs`, `PATCH /jobs` and `GET /jobs/{job_id}` requests removed in favor of export processes. [#153](https://github.com/Open-EO/openeo-api/issues/153)
- `min_parameters` and `dependencies` for parameters in process descriptions returned by `GET /processes`.

### Fixed
- Added missing `Access-Control-Expose-Headers` header to required CORS headers.

## [0.3.1] - 2018-11-06

### Added
- `createProcessGraph` method to client development guidelines.
- JSON file with all specified errors.
- Textual error codes for each specified error.
- Allow setting a plan for `POST /preview`
- Default billing plan in `GET /`. [#141](https://github.com/Open-EO/openeo-api/issues/141)
- Job ID in JSON response for `GET /jobs/{job_id}/results`.

### Changed
- Several optional fields such as `output`, `title` and `description` are now nullable instead of requiring to omit them.
- The output format is not required in `POST /preview` any more and thus allows falling back to the default.
- The `output_format` parameter in `createJob` and `execute` in client development guidelines.
- The `extent` parameters in `filter_bbox` and `filter_daterange` are formally required now.

### Deprecated
- Numeric openEO error codes are soon to be replaced with textual error codes.
- `eo:resolution` in collection bands is a duplicate of `eo:gsd`. Use `eo:gsd` instead.

### Fixed
- Fixed a wrong definition of the header `OpenEO-Costs` in `POST /preview`.
- Fixed typo in method `authenticateOIDC` in client development guidelines.
- Fixed the definition of spatial extents by swapping north and south.
- Replaced the outdated occurrences of `srs` with `crs` in spatial extents.
- Added missing required descriptions to process definitions.
- Added missing error messages.
- Fixed unclear specification for arrays used as process graph arguments.
- Fixed inconsist schema of openEO error responses: Field is now consistently named `message` instead of `description`.

## [0.3.0] - 2018-09-21
First version after proof of concept tackling many major issues. No changelog available.

## [0.0.2] - 2018-03-22
Version for proof of concept. No changelog available.

## [0.0.1] - 2018-02-07
Initial version.

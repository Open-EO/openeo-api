# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0-rc.1 - 2020-01-31

**Note:** The user and developer documentation has been moved to [openeo.org](https://openeo.org/documentation).

### Added

- `GET /`: 
    - Field `production` added to response. [#184](https://github.com/Open-EO/openeo-api/issues/184)
    - Required fields `stac_version` and `id` added to response for STAC compatibility. [#247](https://github.com/Open-EO/openeo-api/issues/247)
    - Links with relation types `terms-of-service` and `privacy-policy` explicitly documented. Clients must handle them properly if present. [#212](https://github.com/Open-EO/openeo-api/issues/212)
- `GET /collections` and `GET /collections/{collectionId}`:
    - New field `deprecated` can be used to indicate outdated collections. Links with relation type `latest-version` can point to the latest version. [#226]( https://github.com/Open-EO/openeo-api/issues/226)
    - Added a Data Cube Dimension of type `bands` to the `cube:dimensions` property. [#208](https://github.com/Open-EO/openeo-api/issues/208)
- `GET /conformance` has been added for OCG API compliance. Back-ends may implement it for compatibility with OGC API clients. 
- `POST /result`: May add a link to a log file in the header. [#214](https://github.com/Open-EO/openeo-api/issues/214)
- `GET /jobs/{job_id}/logs` and `GET /services/{service_id}/logs`: Endpoints that publish logging information. [#214](https://github.com/Open-EO/openeo-api/issues/214)
- `GET /files`, `GET /jobs`, `GET /process_graphs`, `GET /services`: Added `limit` parameter for pagination and clarified how to use links for pagination. [#103](https://github.com/Open-EO/openeo-api/issues/103)
- JSON Schema for the defined schema `subtypes`.

### Changed

- The concept of callbacks has simply been renamed to process graph. Schema format/subtype `callback` has been renamed to `process-graph`. [#216](https://github.com/Open-EO/openeo-api/issues/216)
- Unsupported endpoints are not forced to return a `FeatureUnsupported` (501) error and can return a simple `NotFound` (404) instead.
- If `currency` returned by `GET /` is `null`, `costs` and `budget` are unsupported. `costs` and `budget` fields in various endpoints can be set to `null` (default).
- Official support for [CommonMark 0.29 instead of CommonMark 0.28](https://spec.commonmark.org/0.29/changes.html). [#203](https://github.com/Open-EO/openeo-api/issues/203)
- The parameter `user_id ` has been removed from the endpoints to manage user files (`/files/{user_id}`). [#218](https://github.com/Open-EO/openeo-api/issues/218)
- Schema subtype `band-name` allows common band names, too. [Processes#77](https://github.com/Open-EO/openeo-processes/issues/77)
- Link property `rel` is required.
- OpenAPI string format `url` has been replaced with `uri`.
- Process graphs:
    - `from_argument` has been renamed to `from_parameter`.
    - `callback` has been renamed to `process_graph`.
    - `from_parameter` can access parameters defined in parent scopes.
    - `from_parameter` can be used in the top-level process graph.
    - Process graph variables (objects with `variable_id` etc.) have been removed.
- `GET /jobs`, `GET /jobs/{job_id}`, `GET /services` and `GET /services/{service_id}`: Renamed field `submitted` to `created` for consistency with STAC job results.
- `GET /`: Property `links` is required.
- `GET /service_types`:
    - `parameter` has been renamed to `configuration` to not overlap with `process_parameters`.
    - `variables` has been renamed to `process_parameters` and has a different schema now. [#161](https://github.com/Open-EO/openeo-api/issues/161)
- `GET /processes`:
    - Default values are now specified on the parameter-level, not in the JSON schemas.
    - Multiple data types in parameters or return values are supported as arrays. Using `anyOf` is discouraged.
    - Parameters are defined as array. `parameter_order` is therefore removed and the name is part of the parameter object. [#239](https://github.com/Open-EO/openeo-api/issues/239)
    - Process graph (callback) parameters have a new, more advanced schema, allowing to define more aspects of the process graph parameters. [#239](https://github.com/Open-EO/openeo-api/issues/239)
    - Return values don't require a description any longer.
    - `required` was replaced with `optional` with inverted behavior.
- `GET /collections` and `GET /collections/{collectionId}`: Updated STAC to version 0.9.0. See the [STAC Changelog](https://github.com/radiantearth/stac-spec/blob/master/CHANGELOG.md) for more details. [#247](https://github.com/Open-EO/openeo-api/issues/247), [#204](https://github.com/Open-EO/openeo-api/issues/204).
- `GET /credentials/oidc`: Changed response to support multiple OpenID Connect identity providers ([#201](https://github.com/Open-EO/openeo-api/issues/201)) and clarified workflow overall.
- Bearer token are built from the authentication method, an optional provider id and the token itself. [#219](https://github.com/Open-EO/openeo-api/issues/219)
- `GET /udf_runtimes`: `description` fields don't allow `null` values any longer.
- `GET /output_formats` renamed to `GET /file_formats` to allow listing input file formats. [#215](https://github.com/Open-EO/openeo-api/issues/215)
    - The structure of the response has changed. The former response body for the output formats is now available in the property `output`.
    - The input file formats are now available in the property `input` with the same schema as for output formats.
    - Additionally, each format can have a `title`.
- `GET /jobs/{job_id}/results`:
    - Response body for status code 200 has changed to be a valid STAC Item, allows content type `application/geo+json`.
    - Response body for status code 424 has been extended.

### Deprecated

- The processes should not use the JSON Schema keyword `format` any longer. Instead use the custom keyword `subtype`. [#233](https://github.com/Open-EO/openeo-processes/issues/233)
- PROJ definitions are deprecated in favor of EPSG codes and WKT2. [#58](https://github.com/Open-EO/openeo-processes/issues/58)

### Removed

- Process graph variables. Use Parameter References instead.
- `GET /processes`: `media_type` removed from parameters and return values. Use `contentMediaType` in the JSON Schema instead.
- `GET /job/{job_id}`: Removed property `error`. Request information from `GET /job/{job_id}/logs` instead.
- `GET /job/{job_id}/results`:
    - Metalink XML encoding has been removed. [#205](https://github.com/Open-EO/openeo-api/issues/205)
    - `Expires` header has been removed, use `expires` property in the response body instead.
- `GET /credentials/basic` doesn't return a `user_id`. Instead request it from `GET /me`.
- `GET /collections/{collectionId}`: Removed optional STAC extensions from the API specification. Inform yourself about useful [STAC extensions](https://github.com/radiantearth/stac-spec/tree/master/extensions#list-of-content-extensions) instead. [#176](https://github.com/Open-EO/openeo-api/issues/176)
- `GET /service_types` doesn't support `attributes` any longer.

### Fixed

- Service parameters and attributes in `GET /service_types` and output format parameters in `GET /file_formats` (previously `GET /output_formats`) now have a `type`, which was previously only mentioned in examples.
- `GET /processes`: Parameters `arguments` and `process_graph` can't be used together in process examples.
- `GET /collections`, `GET /processes`: Clarified that pagination is not supported. [#103](https://github.com/Open-EO/openeo-api/issues/103)
- `GET ./well-known/openeo`: Clarified how clients and back-ends should implement well-known discovery. [#202](https://github.com/Open-EO/openeo-api/issues/202)

## [0.4.2] - 2019-06-11

### Added
- Basic JSON Schema for process graph validation.

### Changed
- Updated the process catalog, see the separate changelog.

### Removed
- Disallowed CommonMark in descriptions of process graph variables and process graph nodes.

### Fixed
- Improved documentation with several clarifications, better examples and more.
- SAR Bands had a required but undefined property. [#187](https://github.com/Open-EO/openeo-api/issues/187)
- Clarified how file paths in the URL must be encoded for file handling.
- OpenAPI `nullable` issues:
    - Removed `null` from SAR Bands `enum` for OpenAPI code generator, is handled by `nullable`. [OpenAPI-Specification#1900](https://github.com/OAI/OpenAPI-Specification/issues/1900)
    - `nullable` doesn't combine well with `anyOf`, `allOf` and `oneOf`, therefore placed `nullable` also in one of the sub-schemas.  [OpenAPI-Specification#1368](https://github.com/OAI/OpenAPI-Specification/issues/1368)

## [0.4.1] - 2019-05-29

### Changed
- Updated the process catalog, see the separate changelog.

### Removed
- The property `sar:absolute_orbit` in `GET /collections/{collection_id}` has been removed.
- Sending a Bearer token to `GET /credentials/oidc` is not allowed any longer.

### Fixed
- Improved and clarified the documentation and descriptions.
- `GET /collections/{collection_id}`:
    - `properties` in `GET /collections/{collection_id}` doesn't require any of the integrated STAC extensions any longer.
    - The property `sci:publications` in `GET /collections/{collection_id}` was ported over incorrectly from STAC. The data type has been changed from object to array.
- `GET /jobs/{job_id}/results` was expected to return HTTP status code 424 with an error message, but it was specified in `/jobs/{job_id}/estimate` instead. The definition was moved. [#177](https://github.com/Open-EO/openeo-api/issues/177)
- `path` in `GET` and `PUT` `/files/{user_id}` is required again.
- Fixed several issues in the client development guidelines.

## [0.4.0] - 2019-03-07

### Added
- `GET /jobs/{job_id}/estimate` can return the estimated required storage capacity. [#122](https://github.com/Open-EO/openeo-api/issues/122)
- `GET /jobs/{job_id}` has two new properties:
    - `progress` indicates the batch job progress when running. [#82](https://github.com/Open-EO/openeo-api/issues/82)
    - `error` states the error message when a job errored out.
      `GET /jobs/{job_id}/result` mirrors this error message in a response with HTTP status code 424. [#165](https://github.com/Open-EO/openeo-api/issues/165)
- `GET /.well-known/openeo` allows clients to choose between versions. [#148](https://github.com/Open-EO/openeo-api/issues/148)
- `GET /` (Capabilities):
    - Requires to return a title (`title`), a description (`description`) and the back-end version (`backend_version`). [#154](https://github.com/Open-EO/openeo-api/issues/154)
    - Billing plans have an additional required property `paid`. [#157](https://github.com/Open-EO/openeo-api/issues/157)
    - Should provide a link to the Well-Known URI (`/.well-known/openeo`) in the new `links` property.
- `GET /processes` (Process discovery):
    - Processes can be categorizes with the `category` property.
    - Parameters can be ordered with the `parameter_order` property instead of having a random order.
    - Support for references to other processes in descriptions.
    - Processes and parameters can be declared to be `experimental`.
- `GET /output_formats` and `GET /service_types` can now provide links per entry.
- `GET /udf_runtimes` provide a list of UDF runtime environments. [#87](https://github.com/Open-EO/openeo-api/issues/87)
- `GET /service_types` allows to specify `variables` that can be used in process graphs. [#172](https://github.com/Open-EO/openeo-api/issues/172)

### Changed
- Completely new version of the processes.
- Changed process graph to a flexible graph-like structure, which also allows callbacks. [#160](https://github.com/Open-EO/openeo-api/issues/160)
- Updated `GET /collections` and `GET /collections/{collection_id}` to follow STAC v0.6.2. [#158](https://github.com/Open-EO/openeo-api/issues/158), [#173](https://github.com/Open-EO/openeo-api/issues/173)
- The `process_graph_id` of stored process graphs, the `service_id` of services and the `job_id` of jobs has changed to `id` in responses. [#130](https://github.com/Open-EO/openeo-api/issues/130)
- The `status` property for jobs is now required. 
- `POST /preview` renamed to `POST /result`. [#162](https://github.com/Open-EO/openeo-api/issues/162)
- `GET /` (Capabilities):
    - `version` in the response was renamed to `api_version`.
    - Endpoint paths must follow the openAPI specification. [#128](https://github.com/Open-EO/openeo-api/issues/128)
    - Billing plan descriptions allow CommonMark. [#164](https://github.com/Open-EO/openeo-api/issues/164)
- `/files/{user_id}/{path}` File management:
    - Clarified handling of folders. [#146](https://github.com/Open-EO/openeo-api/issues/146)
    - `GET` method: The `name` property was renamed to `path`. [#133](https://github.com/Open-EO/openeo-api/issues/133)
    - `PUT` method: Returns file meta data with a different response code. [#163](https://github.com/Open-EO/openeo-api/issues/163)
- `GET /processes` (Process discovery):
    - The `name` property of processes has changed to `id`. [#130](https://github.com/Open-EO/openeo-api/issues/130)
    - `mime_type` replaced with `media_type` in the input parameters and return values.
    - The schema for `exceptions` follows the general schema for openEO errors. [#139](https://github.com/Open-EO/openeo-api/issues/139)
    - Changed the structure of `examples`.
- `POST /validation` (Process graph validation):
    - Returns HTTP status code 200 for valid and invalid process graphs and responds with a list of errors. [#144](https://github.com/Open-EO/openeo-api/issues/144)
    - Allowed to call the endpoint without authentication. [#151](https://github.com/Open-EO/openeo-api/issues/151)
- Behavior for `DELETE /jobs/{job_id}/results` and `POST /jobs/{job_id}/results` specified depending on the job status. Clarified status changes in general. [#142](https://github.com/Open-EO/openeo-api/issues/142)
- Improved client development guidelines. [#124](https://github.com/Open-EO/openeo-api/issues/124), [#138](https://github.com/Open-EO/openeo-api/issues/138)

### Removed
- Numeric openEO error codes. Replaced in responses with textual error codes. [#139](https://github.com/Open-EO/openeo-api/issues/139)
- Query parameters to replace process graph variables in `GET /process_graphs/{process_graph_id}`. [#147](https://github.com/Open-EO/openeo-api/issues/147)
- `min_parameters` and `dependencies` for parameters in process descriptions returned by `GET /processes`.
- Replaced output format properties in favor of a `save_result` process, which has resulted in in the removal of:
  - The default output format in `GET /output_formats`. [#153](https://github.com/Open-EO/openeo-api/issues/153)
  - The output format properties in `POST /result` (fka `POST /preview`), `POST /jobs`, `PATCH /jobs` and `GET /jobs/{job_id}` requests. [#153](https://github.com/Open-EO/openeo-api/issues/153)
  - `gis_data_type` (not to be confused with `gis_data_types`) in the parameters of output formats in `GET /output_formats`

### Fixed
- Added missing `Access-Control-Expose-Headers` header to required CORS headers.
- Some endpoints didn't include authentication information.
- `GET /jobs/{job_id}/estimate`: Property `downloads_included` had a wrong default value.

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

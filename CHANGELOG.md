# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - Unreleased
### Added
- ...

### Changed
- More consistent client development guidelines (casing of parameter names). [#124](https://github.com/Open-EO/openeo-api/issues/124)
- `mime_type` replaced with `media_type` in the process catalogue input parameters and return values.
- The schema for `exceptions` defined in process descriptions (`GET /processes`) follows the general schema for openEO errors.
- The `name` property of processes has changed its name to `id` for consistency.

### Removed
- Numeric openEO error codes. Replaced in responses with textual error codes. [#139](https://github.com/Open-EO/openeo-api/issues/139)
- Removed the query parameters to replace process graph variables in `GET /process_graphs/{process_graph_id}`. [#147](https://github.com/Open-EO/openeo-api/issues/147)

### Fixed
- Separated `process_graph` schemas that allow and don't allow process graph variables. [#150](https://github.com/Open-EO/openeo-api/issues/150)

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

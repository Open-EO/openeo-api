# Federation Extension

The openEO API is a specification for interoperable cloud-based processing of large Earth observation datasets.

This is an extension for federation aspects, i.e. where multiple back-ends are exposed as a single API.

- Version: **0.2.0**
- Stability: **experimental**
- Conformance class: `https://api.openeo.org/extensions/federation/0.2.0`

**Note:** This document only documents the additions to the specification.
Extensions can not change or break existing behavior of the openEO API.

## Back-end details

A new required field `federation` is added to `GET /` to enable federation.

### OpenAPI fragment

```yaml
schema:
  type: object
  required:
    - 'federation'
  properties:
    'federation':
      description: >-
        Lists all back-ends that are part of this federation with details.
        They keys of the object are the unique identifiers for the back-ends that are returned in sub-sequent requests (see below).
      type: object
      minProperties: 2
      additionalProperties:
        type: object
        required:
          - url
        properties:
          url:
            type: string
            format: uri
            description: >-
              URL to the versioned API endpoint of the back-end,
              so a URL that is available through well-known discovery on the back-end.
            example: https://openeo.provider.org/api/v1/
          title:
            type: string
            description: Name of the back-end.
          description:
            type: string
            description: A description of the back-end and its specifics.
          status:
            type: string
            enum:
              - online
              - offline
            description: Current status of the back-ends.
            default: online
          last_status_check:
            type: string
            format: date-time
            description: The time at which the status of the back-end was checked last.
          last_successful_check:
            type: string
            format: date-time
            nullable: true
            description: >-
              If the `status` is `offline`: The time at which the back-end was checked and available the last time
              or `null` when the back-end was never observed to be available.
              Otherwise, this is equal to the property `last_status_check`.
          experimental:
            type: boolean
            description: >-
              Declares the back-end to be experimental, which means that
              it is likely to change or may produce unpredictable behaviour.
            default: false
          deprecated:
            type: boolean
            description: |-
              Declares the back-end to be deprecated with the potential
              to be removed in any of the next versions.
            default: false
```

### Example

```json
{
  "api_version": "1.3.0",
  "federation": {
    "vito": {
      "title": "VITO",
      "url": "https://openeo.vito.be"
    },
    "eodc": {
      "title": "EODC",
      "url": "https://openeo.eodc.eu"
    },
    "wwu": {
      "title": "WWU Münster",
      "url": "https://openeo.wwu.de",
      "status": "offline",
      "description": "Experimental integration of the WWU HPC",
      "experimental": true
    }
  },
  ...
}
```

## Resources supported only by a subset of back-ends

Discoverable resources can explicitly list the subset of back-ends that support or host the exposed resource or functionality with the property `federation:backends`.

Schema-wise, this only applies to resources that are defined as an object and allow to contain additional properties.
For example (**not** comprehensive):

- `GET /collections`
- `GET /collections/{id}`
- `GET /processes` (global, per process, per parameter)
- `GET /file_formats` (global, per file format)
- `GET /service_types` (per service)
- `GET /udf_runtimes` (per UDF runtime, per version)
- `POST /validation` (the back-ends that can run the process, see below)
- `GET /files`
- `GET /process_graphs`
- `GET /process_graphs/{id}`
- `GET /jobs`
- `GET /jobs/{job_id}` (the back-ends that generated the result)
- `GET /jobs/{job_id}/results` (the back-ends that generated the result)
- `GET /services`
- `GET /services/{id}` (the back-ends that host the service)

This can also be embedded deeply into a hierarchical structure, e.g. for process or file format parameters.

```yaml
schema:
  type: object
  properties:
    'federation:backends':
      description: >-
        Lists the subset of back-ends that support or host the resource.
        If not given, all back-ends support the resource.
      type: array
      minItems: 1
      items:
        type: string
        description: The ID of a back-end.
```

**Note:** In Collections this should generally be provided on the top-level of the object.

### Validation

If this property is returned through the `POST /validation` endpoint, it has the meaning as listed below.
This also covers the case where the federation supports splitting a process into pieces so that different parts can run on different back-ends.

- Endpoint returns *without* errors:
  - `federation:backends` is included in the response: The listed back-ends support the workflow (either partially if splitting is supported, or in full).
  - `federation:backends` is *not* included in the response: At least one of the back-ends support the workflow.
- Endpoint returns errors:
  - `federation:backends` is included in the response: The listed back-ends were checked and none of the back-ends can run the workflow as is (neither splitted if supported, nor in full).
  - `federation:backends` is *not* included in the response: the workflow could not be validated successfully by any of the back-ends or the federation component itself. This includes any kind of failed validation attempt, including network and server errors.

### Examples

#### Process

```json
{
  "process_id": "example",
  "federation:backends": ["vito", "eodc"],
  "parameters": [
    {
      "name": "parameter1",
      "description": "A parameter supported by both back-ends...",
      "schema": {}
    },
    {
      "name": "proprietary_parameter",
      "description": "A parameter supported only by EODC.",
      "federation:backends": ["eodc"],
      "schema": {}
    }
  ]
  ...
}
```

#### Collection

```json
{
  "stac_version": "1.0.0",
  "id": "example",
  "description": "...",
  "federation:backends": ["vito", "eodc"],
  ...
}
```

## Temporarily or unintentionally unavailable resources

Resources and back-ends can be temporarily or unintentionally unavailable.
It is especially important to communicate to users missing resources when compiling a **list of resources** across multiple back-ends.
Clients will assume that all lists of resources are a combination of all back-ends listed under `federation` in `GET /`.
Federated APIs can expose if any of the back-ends was not available when building the resource listing response with the property `federation:missing`.

Examples of where this could apply to (**not** comprehensive):

- `GET /collections`
- `GET /processes`
- `GET /file_formats`
- `GET /process_graphs`
- `GET /files`
- `GET /jobs`
- `GET /jobs/{job_id}`
- `GET /jobs/{job_id}/results`
- `GET /jobs/{job_id}/logs`
- `GET /services`

### OpenAPI fragment

```yaml
schema:
  type: object
  properties:
    'federation:missing':
      description: >-
        Lists all back-ends that were unexpectedly unavailable during compilation of the response.
        If not given or empty, all back-ends supporting this endpoint were considered for creating the response.
        Back-ends that are listed as offline in the capabilities still need to be listed here.
      type: array
      items:
        type: string
        description: The ID of a back-end.
```

### Example

```json
{
  "federation:missing": ["wwu"],
  "collections": [...],
  "links": [...]
}
```

## Endpoints that can't list federation details

The following endpoints define the resources (UDF runtimes / service types) at the top level of their response as key-value pairs.
Consequently, they are not extensible with additional properties for federation purposes.

- `GET /udf_runtimes`
- `GET /service_types`

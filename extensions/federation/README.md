# Federation Extension

The openEO API is a specification for interoperable cloud-based processing of large Earth observation datasets.

This is an extension for federation aspects, i.e. where multiple back-ends are exposed as a single API.

Version: **0.1.0**
Stability: **experimental**

**Note:** This document only documents the additions to the specification.
Extensions can not change or break existing behavior of the openEO API.

## Backend details

A new required field `federated:backends` is added to `GET /`:

```yaml
schema:
  type: object
  required:
    - 'federation:backends'
  properties:
    'federation:backends':
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
              URL to the API of the back-end, without the `/.well-known/openeo`
              suffix.
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
```

Example:

```json
{
  "api_version": "1.1.0",
  "federation:backends": {
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
      "description": "Experimental integration of the WWU HPC"
    }
  },
  ...
}
```

## Lists of resources

Clients will assume that all lists of resources (e.g. collections, processes, jobs, ...) are the combined from all back-ends listed in `GET /`. Federated APIs can expose if any of the back-ends is not available and thus is not part of the response.

```yaml
schema:
  type: object
  properties:
    'federation:missing':
      description: >-
          Lists all back-ends that were not considered in the response (e.g. because they were not accessible).
        If not given or empty, all back-ends were considered for creating the response.
        Back-ends that were listed as offline in the capabilities still need to be listed here.
      type: array
      items:
        type: string
        description: The IDs of the back-ends that are not present in the response.
```

Example:

```json
{
  "federation:missing": ["wwu"],
  "collections": [...],
  "links": [...]
}
```

Please note that this does not apply to `GET /udf_runtimes` and `GET /service_types`, which can only expose the availibility per UDF runtime / service type.

## Resources supported only by a subset of back-ends

Every discoverable resource that is defined as an object and allows to contain additional properties, can list the backends that support or host the exposed resource/functionality (e.g. collections, processes, process parameters, file formats, file format parameters, services, jobs, ...)

```yaml
schema:
  type: object
  properties:
    'federation:hosted':
      description: >-
        Lists all back-ends that support or host the resource.
        If not given, all back-ends support the resource.
      type: array
      minItems: 1
      items:
        type: string
        description: The IDs of the back-ends that are not present in the response.
```

Example:

```json
{
  "process_id": "example",
  "federation:hosted": ["vito", "eodc"],
  "parameters": [
    {
      "name": "parameter1",
      "description": "A parameter supported by both back-ends...",
      "schema": {}
    },
    {
      "name": "proprietary_parameter",
      "description": "A parameter supported only by EODC.",
      "federation:hosted": ["eodc"],
      "schema": {}
    }
  ]
  ...
}
```
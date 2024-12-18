# Processing Parameters Extension

The Processing Parameters Extension to the openEO API provides an interface to explore and handle additional processing options that a back-end can offer for the three processing modes (synchronous processing, batch jobs, secondary web services).

- Version: **0.1.0**
- Stability: **experimental**
- [OpenAPI document](openapi.yaml)
- Conformance class: `https://api.openeo.org/extensions/processing-parameters/0.1.0`

**Note:** This document only documents the additions to the specification.
Extensions can not change or break existing behavior of the openEO API.

This extension adds a new endpoint (`GET /processing_options`, see [OpenAPI document](openapi.yaml))
to discover the additional processing options that a back-end offers.

Additionally, this extension allows to provide specific default values for user-defined processes (UDPs, see below).

In both cases, the parameters and its values are provided separately for each processing mode.

## Processing Parameters in UDPs

UDPs can provide default values for specific processing parameters.

The values for each parameter are provided  separately for each processing mode.
The following properties are added to the top-level of a UDP for the respective processing modes:

- `default_synchronous_parameters` for synchronous processing
- `default_job_parameters` for batch jobs
- `default_service_parameters` for secondary web services

The schema for each of these properties is:

```yaml
type: object
additionalProperties:
  description: Any type
```

The keys of the object are the respecive parameter names.
The values of the object are the (default) values for the parameters.
Schematic restrictions are not defined for the object, but the schemas for the parameters as defined in `GET /processing_options` apply to the given values.
These values provide the defaults unless a user overrides them in the actual data processing request (e.g. `POST /jobs`, see below).

## Resolving parameters

Due to the variety of places where processing parameters can be provided, the following
list defines how the parameters must be resolved. The prioritization is as follows:

1. If present, use the parameter specified in the processing request directly (e.g. in `POST /jobs` as a top-level property)
2. If present, use the default parameter specified in the UDP
3. Otherwise, use the default value for the parameter as specified in `GET /processing_options`

"Present" means that the property is present in the JSON representation regardless of the value given, i.e.
properties are present if an empty string, an empty array, an empty object, `false`, `0`, or `null` are provided.

Unrecognized/unknown parameters that are provided through UDPs must be ignored by backends.

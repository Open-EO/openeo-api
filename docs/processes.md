# Processes

A process is an operation that performs a specific task, see the [glossary](glossary.md) for a detailed definition. It consists of a name, a set of parameters, a return type and may throw errors or exceptions. In openEO, processes are used to build a chain of processes ([process graph](processgraphs.md)), which can be applied to EO data to derive your own findings from the data.

## Core processes

There are some processes that we define to be core processes that are pre-defined and back-ends SHOULD follow these specifications to be interoperable. Not all processes need to be implemented by all back-ends.

See the **[process reference](processreference.md)** for pre-defined processes.

## Defining processes

Any back-end provider can either implement a set of pre-defined processes (STRONGLY RECOMMENDED) or define new processes for their domain.

To define new processes, back-end providers MUST follow the `process` schema in the API specification. This includes:

* Choosing a intuitive and ideally unique process name consisting of only letters (a-z), numbers and underscores.
* Defining the parameters and their exacts (JSON) schemes.
* Specifying the return value of a process also with a (JSON) schema.
* Providing examples or compliance tests.
* Trying to make the process universially usable so that other back-end providers or openEO can adopt it.

## openEO specific formats

In addition to the native data formats specified by JSON schema, openEO defines a set of specific formats that should be re-used in process schema definitions:

| Format Name          | Data type | Description |
| -------------------- | --------- | ----------- |
| `callback`           | object    | An openEO process graph that is passed as an argument and is expected to be executed by the process. |
| `date`               | string    | Date only representation, as defined for `full-date` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). The time zone is UTC. |
| `date-time`          | string    | Date and time representation, as defined for `date-time` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). |
| `epsg-code`          | integer   | Specifies details about cartographic projections as [EPSG](http://www.epsg.org) code. |
| `geojson`            | object    | GeoJSON as defined by [RFC 7946](https://tools.ietf.org/html/rfc7946). [JSON Schemes for validation are available.](https://github.com/geojson/schema) |
| `proj-definition`    | string    | Specifies details about cartographic projections as [PROJ](https://proj4.org) definition. |
| `raster-cube`        | object    | A raster data cube, an image collection stored at the back-end. Different back-ends have different internal representations for this data structure. |
| `temporal-intervals` | array     | An array of two-element arrays, which contains temporal left-closed intervals. For more information see the parameter `intervals` in the process `aggregate_temporal`. |
| `time`               | string    | Time only representation, as defined for `full-time` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Although [RFC 3339 prohibits the hour to be '24'](https://tools.ietf.org/html/rfc3339#section-5.7), this definition allows the value '24' for the hour as end time in an interval in order to make it possible that left-closed time intervals can fully cover the day. |
| `vector-cube`        | object    | A vector data cube, a vector collection stored at the back-end. Different back-ends have different internal representations for this data structure |
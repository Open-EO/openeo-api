# Processes

A process is an operation that performs a specific task, see the [glossary](glossary.md) for a detailed definition. It consists of a name, a set of parameters, a return type and may throw errors or exceptions. In openEO, processes are used to build a chain of processes ([process graph](processgraphs.md)), which can be applied to EO data to derive your own findings from the data.

## Core processes

There are some processes that we define to be core processes that are pre-defined and back-ends SHOULD follow these specifications to be interoperable. Not all processes need to be implemented by all back-ends.

See the **[process reference](processreference.md)** for pre-defined processes.

## Defining processes

Any back-end provider can either implement a set of pre-defined processes (STRONGLY RECOMMENDED) or define new processes for their domain.

To define new processes, back-end providers should consider:

* The name is the identifier for the process and MUST only contain a forward slash `/`. 
* Each parameter has a name and the content follows a schema.
* The content returned by a process also follows a schema.
* The schema usually defines the data type and a format according to JSON schema. There are openEO specific formats defined below.

## openEO specific formats

In addition to the native data formats specified by JSON schema, openEO defines a set of specific formats that should be re-used in process schema definitions:

| Format Name   | Description |
| ------------- | ----------- |
| `callback`    | An openEO process graph that is passed as an argument and is expected to be execute by the process. |
| `date`        | Date only representation, as defined for `full-date` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). The time zone is UTC. |
| `date-time`   | Date and time representation, as defined for `date-time` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). |
| `geojson`     | GeoJSON as defined by [RFC 7946](https://tools.ietf.org/html/rfc7946). [JSON Schemas for validation are available.](https://github.com/geojson/schema) |
| `raster-cube` | A raster data cube, an image collection stored at the back-end. Different back-ends have different internal representations for this data structure. |
| `temporal-intervals` | An array of two-element arrays, which contains temporal left-closed intervals. For more information see the parameter `intervals` in the process `aggregate_temporal`. |
| `time`        | Time only representation, as defined for `full-time` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Although [RFC 3339 prohibits the hour to be '24'](https://tools.ietf.org/html/rfc3339#section-5.7), this definition allows the value '24' for the hour as end time in an interval in order to make it possible that left-closed time intervals can fully cover the day. |
| `vector-cube` | A vector data cube, a vector collection stored at the back-end. Different back-ends have different internal representations for this data structure |
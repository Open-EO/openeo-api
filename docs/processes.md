# Processes

A process is an operation that performs a specific task, see the [glossary](glossary.md) for a detailed definition. It consists of an id (the identifying name of the process), a set of parameters, a return type and may throw errors or exceptions. In openEO, processes are used to build a chain of processes ([process graph](processgraphs.md)), which can be applied to EO data to derive your own findings from the data.

## Core processes

There are some processes that we define to be core processes that are pre-defined and back-ends SHOULD follow these specifications to be interoperable. Not all processes need to be implemented by all back-ends.

See the **[process reference](processreference.md)** for pre-defined processes.

## Defining processes

Any back-end provider can either implement a set of pre-defined processes (STRONGLY RECOMMENDED) or define new processes for their domain.

To define new processes, back-end providers MUST follow the `process` schema in the API specification. This includes:

* Choosing a intuitive and ideally unique name as process id, consisting of only letters (a-z), numbers and underscores.
* Defining the parameters and their exacts (JSON) schemes.
* Specifying the return value of a process also with a (JSON) schema.
* Providing examples or compliance tests.
* Trying to make the process universially usable so that other back-end providers or openEO can adopt it.

## openEO specific formats

In addition to the native data formats specified by JSON schema, openEO defines a set of specific formats that should be re-used in process schema definitions:

| Format Name               | Data type | Description |
| ------------------------- | --------- | ----------- |
| `band-name`               | string    | A band name available in the data cube. |
| `bounding-box`            | object    | A bounding box with the required fields `west`, `south`, `east`, `north` and optionally `base`, `height`, `crs`. The `crs` is a EPSG code or PROJ definition. |
| `callback`                | object    | An openEO process graph that is passed as an argument and is expected to be executed by the process. Callback parameters are specified in a `parameters` property (see chapter "Callbacks" below). |
| `collection-id`           | string    | A collection id from the list of supported collections. Pattern: `^[A-Za-z0-9_\-\.~/]+$` |
| `date`                    | string    | Date only representation, as defined for `full-date` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). The time zone is UTC. |
| `date-time`               | string    | Date and time representation, as defined for `date-time` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). |
| `epsg-code`               | integer   | Specifies details about cartographic projections as [EPSG](http://www.epsg.org) code. |
| `geojson`                 | object    | GeoJSON as defined by [RFC 7946](https://tools.ietf.org/html/rfc7946). [JSON Schemes for validation are available.](https://github.com/geojson/schema) |
| `job-id`                  | string    | A batch job id, either one of the jobs a user has stored or a publicly available job. Pattern: `^[A-Za-z0-9_\-\.~]+$` |
| `kernel`                  | array     | Image kernel, a multi-dimensional array of numbers. |
| `output-format`           | string    | An output format supported by the back-end. |
| `output-format-options`   | object    | Key-value-pairs with arguments for the output format options supported by the back-end. |
| `process-graph-id`        | string    | A process graph id, either one of the process graphs a user has stored or a publicly available process graph. Pattern: `^[A-Za-z0-9_\-\.~]+$` |
| `process-graph-variables` | object    | Key-value-pairs with values for variables that are defined by the process graph. The key of the pair is the `variable_id` for the value specified. |
| `proj-definition`         | string    | Specifies details about cartographic projections as [PROJ](https://proj4.org) definition. |
| `raster-cube`             | object    | A raster data cube, an image collection stored at the back-end. Different back-ends have different internal representations for this data structure. |
| `temporal-interval`       | array     | A two-element array, which describes a left-closed temporal interval. The first element is the start of the date and/or time interval. The second element is the end of the date and/or time interval. The specified temporal strings follow the formats `date-time`, `date` (see above) and `time` (see below). |
| `temporal-intervals`      | array     | An array of two-element arrays, each being an array with format `temporal-interval` (see above). |
| `time`                    | string    | Time only representation, as defined for `full-time` by [RFC 3339 in section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). Although [RFC 3339 prohibits the hour to be '24'](https://tools.ietf.org/html/rfc3339#section-5.7), this definition allows the value '24' for the hour as end time in an interval in order to make it possible that left-closed time intervals can fully cover the day. |
| `vector-cube`             | object    | A vector data cube, a vector collection stored at the back-end. Different back-ends have different internal representations for this data structure |

### Callbacks

A callback is defined by setting the `type` to `object` and the `format` to `callback`. Additionally, it must have a property `parameters` (a custom JSON Schema keyword). `parameters` must be an object with the keys being the callback parameter names and the values being a valid JSON Schema again.

A schema for a callback with two parameters `dimension` (a string) and `data` (an array of numbers) could be defined as follows:

```json
{
  "type": "object",
  "format": "callback",
  "parameters": {
    "dimension": {
      "description": "Name of the dimension",
      "type": "string"
    },
    "data": {
      "description": "Data for the dimension",
      "type": "array",
      "items": {
        "type": "number"
      }
    }
  }
}
```


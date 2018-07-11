# Processes

A process is defined in the API specification. It is an operation that performs a specific task on a set of parameters and returns a result. It's definition includes a name, a set of parameters, a return type, a set of possible errors or exceptions and some other metadata. 

* The name is the identifier for the process and MUST never contain a forward slash `/`. 
* Each parameter has a name and the valid content follows a schema.
* The content returned by a process also follows a schema.
* The schema usually defines the data type and a format according to JSON schema. There are openEO specific formats defined below.

## openEO specific formats

TBD

## Core Processes

There are some processes that we define to be core processes that should be implemented by all back-ends:

* get_data
* filter_bands
* filter_daterange
* process_graph
* _to be continued..._

_Note:_ Currently there are only few defined processes. Those are currently only meant as an example how future documentation of processes may look like.

### get_data

Filters and selects a single dataset provided by the back-end.

#### Arguments

Any of the properties of a dataset, e.g.

- `data_id`: Filter by data id
- `extent`: Filter by extent
- `time`: Filter by time
- `bands`: Filter by band ids
- ...

The back-end provider decides which of the potential datasets is the most relevant one to be selected.

#### Examples

```
{
  "process_id": "get_data",
  "data_id":"Sentinel2A-L1C"
}
```

```
{
  "process_id": "get_data",
  "platform": "landsat-7",
  "sensor": "modis", 
  "derived_from": null
}
```

### filter_bands

Allows to extract one or multiple bands of multi-band raster image collection. Bands can be chosen either by band id, band name or by wavelength.

#### Arguments

* `imagery` *(required)*: Image collection to filter

And one of:

* `bands`: string or array of strings containing band ids.
* `names`: string or array of strings containing band names.
* `wavelengths`: number or two-element array of numbers containing a wavelength or a minimum and maximum wavelength respectively.

#### Examples

```
{
  "process_id":"filter_bands",
  "imagery":{
    "process_id":"get_data",
    "data_id":"Sentinel2A-L1C"
  },
  "bands":"1"
}
```

```
{
  "process_id":"filter_bands",
  "imagery":{
    "process_id":"get_data",
    "data_id":"Sentinel2A-L1C"
  },
  "wavelengths":[
    1300,
    2000
  ]
}
```

### filter_daterange

Allows to filter an image collection by temporal extent.

### Arguments

* `imagery` *(required)*: Image collection to filter

And at least one of:

* `from`: Includes all data newer than the specified ISO 8601 date or date-time with simultaneous consideration of `to`.
* `to`: Includes all data older than the specified ISO 8601 date or date-time with simultaneous consideration of `from`.

#### Examples

```
{
  "process_id":"filter_daterange",
  "imagery":{
    "process_id":"get_data",
    "data_id":"Sentinel2A-L1C"
  },
  "from":"2017-01-01",
  "to":"2017-01-31"
}
```

### process_graph

Another process graph can be referenced with the process `process_graph`. This could even be an externally hosted process graph.

#### Arguments

* `uri` *(required)*: An URI to a process graph.
* `variables`: An object holding key-value-pairs with values for variables that are defined by the process graph. The key of the pair has to be the corresponding `variable_id` for the value specified. The replacement for the variable is the value of the pair.

#### Examples

```
{
  "process_id":"process_graph",
  "uri":"http://otherhost.org/api/v1/users/12345/process_graphs/abcdef",
  "variables": {
  	"data_id":"Sentinel2A-L1C"
  }
}
```

`data_id` is a variable defined by the process graph stored at `http://otherhost.org/api/v1/users/12345/process_graphs/abcdef` and should be replaced with the string `Sentinal2A-L1C`.

### _to be continued..._
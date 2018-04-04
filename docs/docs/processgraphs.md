# Process graphs

_Early work in progress, please contribute by adding [issues](https://github.com/Open-EO/openeo-api/issues)._

A process graph includes specific process calls, i.e. references to one or more processes including specific values for input arguments similar to a function call in programming. However, process graphs can chain multiple processes. In particular, arguments of processes in general can be again (recursive) process graphs, input datasets, or simple scalar or array values.

## Schematic definition

### Process

A single process in a process graph is defined as follows:

```
<Process> := {
  "process_id": <string>,
  "args": <ArgumentSet>
}
```
A process must always contain two key-value-pairs named `process_id` and `args` and no other elements.

`process_id` can currently contain three types of processes:

* Backend-defined processes, which are listed at `GET /processes`, e.g. `filter_bands`.
* User-defined process graphs, which are listed at `GET /users/{user_id}/process_graphs`. 
  They are prefixed with `/user/`, e.g. `/user/my_process_graph`.
* User-defined functions (UDF), which is one of the predefined [UDF types](udfs.md) and can be explored at `GET /udf_runtimes/{lang}/{udf_type}`. UDFs are prefixed with `/udf` and additionally contain the runtime and the process name separated by `/`, e.g. `/udf/Python/apply_pixel`.

**Example 1:**

A full process graph definition.

```
{
  "process_id":"min_time",
  "args":{
    "imagery":{
      "process_id":"/user/custom_ndvi",
      "args":{
        "imagery":{
          "process_id":"filter_daterange",
          "args":{
            "imagery":{
              "process_id":"filter_bbox",
              "args":{
                "imagery":{
                  "process_id":"get_data",
                  "args": {
                    "data_id": "S2_L2A_T32TPS_20M"
                  }
                },
                "left":652000,
                "right":672000,
                "top":5161000,
                "bottom":5181000,
                "srs":"EPSG:32632"
              }
            },
            "from":"2017-01-01",
            "to":"2017-01-31"
          }
        },
        "red":"B04",
        "nir":"B8A"
      }
    }
  }
}
```

### Argument Set

An argument set for a process is defined as follows:

```
<ArgumentSet> := {
  <Key>: <Value>
}
```

Where a key (`<Key>`) can be any valid JSON key and a value is defined as:
```
<Value> := <string|number|array|boolean|null|Process>
```

*Note:* string, number, array, boolean and null are the primitive data types supported by JSON. An array must always contain *one data type only* and is allowed to contain the data types allowed for `<Value>`, too. In consequence, the objects allowed to be part of an array are processes only.

*Note:* The expected names of arguments are defined by the process descriptions, which can be discovered at `GET /processes` and `GET /udf_runtimes/{lang}/{udf_type}`. Therefore, the key name for a key-value-pair holding an image collection as value doesn't necessarily need to be named `imagery`. The name depends on the name of the corresponding process argument the image collection is assigned to. Example 3 demonstrates this by using `collection` as a key once. 

**Example 2:**
```
{
  "imagery":{
    "process_id":"filter_daterange",
    "args":{
      "imagery":{
        "process_id":"get_data",
        "args": {
          "data_id": "Sentinel2A-L1C"
        }
      },
      "from":"2017-01-01",
      "to":"2017-01-31"
    }
  }
}
```

**Example 3:**

If a process needs multiple processes as input, it is allowed to use arrays of the respective types.

```
{
  "imagery":{
    "process_id":"union",
    "args":{
      "collection":[
        {
          "process_id":"filter_bands",
          "args":{
            "imagery":{
              "process_id":"get_data",
              "args": {
                "data_id": "Sentinel2-L1C"
              }
            },
            "bands":8
          }
        },
        {
          "process_id":"filter_bands",
          "args":{
            "imagery":{
              "process_id":"get_data",
              "args": {
                "data_id": "Sentinel2-L1C"
              }
            },
            "bands":5
          }
        }
      ]
    }
  }
}
```

## Core processes

There are some processes that we define to be core processes that should be implemented by all back-ends:

* filter_bands
* filter_daterange
* process_graph
* _to be continued..._

_Note:_ Currently there are only few defined processes. Those are currently only meant as an example how future documentation of processes might look like and to supplement the schematic definition above.

_Limitation:_ Process names (process ids) must never contain a forward slash `/`.

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
  "args": {
    "data_id":"Sentinel2A-L1C"
  }
}
```

```
{
  "process_id": "get_data",
  "args": {
    "platform": "landsat-7",
    "sensor": "modis", 
    "derived_from": null
  }
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
  "process_id": "filter_bands",
  "args": {
    "imagery":{
      "process_id":"get_data",
      "args": {
        "data_id": "Sentinel2A-L1C"
      }
    },
    "bands":1
  }
}
```

```
{
  "process_id": "filter_bands",
  "args": {
    "imagery":{
      "process_id":"get_data",
      "args": {
        "data_id": "Sentinel2A-L1C"
      }
    },
    "wavelengths":[1300,2000]
  }
}
```

### filter_daterange

Allows to filter an image collection by temporal extent.

#### Arguments

* `imagery` *(required)*: Image collection to filter

And at least one of:

* `from`: Includes all data newer than the specified ISO 8601 date or date-time with simultaneous consideration of `to`.
* `to`: Includes all data older than the specified ISO 8601 date or date-time with simultaneous consideration of `from`.

#### Examples

```
{
  "process_id":"filter_daterange",
  "args":{
    "imagery":{
      "process_id":"get_data",
      "args": {
        "data_id": "Sentinel2A-L1C"
      }
    },
    "from":"2017-01-01",
    "to":"2017-01-31"
  }
}
```

### process_graph

Another process graph can be referenced with the process `process_graph`. This could even be an externally hosted process graph.

#### Arguments

* `imagery` *(required)*: Image collection to apply the process graph to
* `uri` *(required)*: An URI to a process graph.

#### Examples

```
{
  "process_id":"process_graph",
  "args":{
    "imagery":{
      "process_id":"get_data",
      "args": {
        "data_id": "Sentinel2A-L1C"
      }
    },
    "uri":"http://otherhost.org/api/v1/users/12345/process_graphs/abcdef"
  }
}
```

### _to be continued..._
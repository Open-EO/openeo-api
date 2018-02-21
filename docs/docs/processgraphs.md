# Process graphs

_Early work in progress, please contribute by adding [issues](https://github.com/Open-EO/openeo-api-poc/issues)._

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

**Example 1:**

```
{
  "process_id":"min_time",
  "args":{
    "imagery":{
      "process_id":"NDVI",
      "args":{
        "imagery":{
          "process_id":"filter_daterange",
          "args":{
            "imagery":{
              "process_id":"filter_bbox",
              "args":{
                "imagery":{
                  "product_id":"S2_L2A_T32TPS_20M"
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

Whereas a key (`<Key>`) can be any valid JSON key and a value is defined as:
```
<Value> := <string|number|array|boolean|null|Process|ImageCollection>
```

*Note:* string, number, array, boolean and null are the primitive data types supported by JSON. An array must always contain *one data type only* and is allowed to contain the data types allowed for `<Value>`, too. In consequence, the objects allowed to be part of an array are processes and image collections only.

**Example 2:**
```
{
  "imagery":{
    "process_id":"filter_daterange",
    "args":{
      "imagery":{
        "product_id":"Sentinel2A-L1C"
      }
    },
    "from":"2017-01-01",
    "to":"2017-01-31"
  }
}
```
**Example 3:**

If a process needs multiple processes or image collections as input, it is allowed to use arrays of the respective types.

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
              "product_id":"Sentinel2-L1C"
            },
            "bands":8
          }
        },
        {
          "process_id":"filter_bands",
          "args":{
            "imagery":{
              "product_id":"Sentinel2-L1C"
            },
            "bands":5
          }
        }
      ]
    }
  }
}
```

### Image Collection

An image collection as input dataset is defined as follows:

```
<ImageCollection> := {
  "product_id": <string>
}
```
*Note:* The key name for a key-value-pair holding an image collection as value doesn't necessarily need to be named `imagery`. The name depends on the name of the corresponding process argument the image collection is given to. Example 3 demonstrates this by using `collection` as a key once.

**Example 4:**

```
{
  "product_id":"Sentinel2A-L1C"
}
```

## Core processes

There are some processes that we define to be core processes that should be implemented by all back-ends:

* filter_bands
* process_graph
* _to be continued..._

### filter_bands

Allows to extract one or multiple bands of multi-band raster image collection. Bands can be chosen either by band id, band name or by wavelength.

#### Arguments

* `imagery`*: Image collection to filter

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
      "product_id":"Sentinel2A-L1C"
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
      "product_id":"Sentinel2A-L1C"
    },
    "wavelengths":[1300,2000]
  }
}
```
### process_graph

Another process graph can be referenced with the process `process_graph`. This could even be an externally hosted process graph.

#### Arguments

* `imagery`*: 
* `uri`*: An URI to a process graph.

#### Examples

```
{
  "process_id":"process_graph",
  "args":{
    "imagery":{
      "product_id":"Sentinel2A-L1C"
    },
    "uri":"http://otherhost.org/api/v1/users/12345/process_graphs/abcdef"
  }
}
```
### _to be continued..._
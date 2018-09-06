# Process graphs

A process graph includes specific process calls, i.e. references to one or more processes including specific values for input arguments similar to a function call in programming. However, process graphs can chain multiple processes. In particular, arguments of processes in general can be again (recursive) process graphs, input datasets, or simple scalar or array values.

## Schematic definition

A process graph is defined to consist of chained processes:

```
<ProcessGraph> := <Process>
```

An argument value of a process can hold a Process again. This allows chaining of processes.

### Process

A single process in a process graph is defined as follows:

```
<Process> := {
  "process_id": <string>,
  "process_description": <string>,
  "<ArgumentName>": <Value>,
  ...
}
```
A process MUST always contain a key-value-pair named `process_id` and MAY contain a `process_description`.  It MAY hold an arbitrary number of additional elements as arguments for the process.

`process_id` can currently contain three types of processes:

* Backend-defined processes, which are listed at `GET /processes`, e.g. `filter_bands`.
* User-defined process graphs, which are listed at `GET /users/{user_id}/process_graphs`. 
  They are prefixed with `/user/`, e.g. `/user/my_process_graph`.
* User-defined functions (UDF) are prefixed with `/udf` and additionally contain the runtime and the process name separated by `/`, e.g. `/udf/Python/apply_pixel`.

### Arguments

A process can have an arbitrary number of arguments.

The key `<ArgumentName>` can be any valid JSON key, but it is RECOMMENDED to use [snake case](https://en.wikipedia.org/wiki/Snake_case) and limit the characters to `a-z`, `0-9` and `_`. `<ArgumentName>` MUST NOT use the names `process_id` or `process_description` as it would result in a naming conflict.

A value is defined as follows:

```
<Value> := <string|number|boolean|null|array|object|Process|Variable>
```

!!! note
    The specified data types except `Process` and `Variable` (see definition above) are the native data types supported by JSON. Some limitations apply:
    * An array MUST always contain *one data type only* and is allowed to contain the data types allowed for `<Value>`.
    * Objects are not allowed to have keys with the following names:
      * `process_id`, except for objects of type `Process`
      * `variable_id`, except for objects of type `Variable`

!!! caution
    The expected names of arguments are defined by the process descriptions, which can be discovered with calls to `GET /processes`. Therefore, the key name for a key-value-pair holding an image collection as value doesn't necessarily need to be named `imagery`. The name depends on the name of the corresponding process argument the image collection is assigned to. Example 2 demonstrates this by using `collection` as a key once. 

### Variables

Process graphs can also hold a variable, which can be filled in later. For shared process graphs this can be useful to make them more portable, e.g in case a back-end specific product name would be stored with the process graph.

Variables are defined as follows:

```
<Process> := {
  "variable_id": <string>,
  "description": <string>,
  "type": <string>,
  "default": <Value>
}
```

The value for `type` is the expected data type for the content of the variable and MUST be one of `string` (default), `number`, `boolean`, `array` or `object`.

The value for `variable_id` is the name of the variable and can be any valid JSON key, but it is RECOMMENDED to use [snake case](https://en.wikipedia.org/wiki/Snake_case) and limit the characters to `a-z`, `0-9` and `_`.

Whenever no value for the variable is defined, the `default` value is used. `<Value>` can be used as defined above, but MUST NOT be a `Variable`. Values for variables can be specified in the query string or body of endpoints supporting variables. See the API reference for more information.

## Examples

**Example 1:** A full process graph definition including a variable for the collection `name`.

``` json
{
  "process_id":"min_time",
  "imagery":{
    "process_id":"/udf/Python/custom_ndvi",
    "imagery":{
      "process_id":"filter_daterange",
      "imagery":{
        "process_id":"filter_bbox",
        "imagery":{
          "process_id":"get_collection",
          "name":{
            "variable_id":"product",
            "description":"Identifier of the collection",
            "type":"string",
            "default":"S2_L2A_T32TPS_20M"
          }
        },
        "left":652000,
        "right":672000,
        "top":5161000,
        "bottom":5181000,
        "srs":"EPSG:32632"
      },
      "extent":"2017-01-01/2017-01-31"
    },
    "red":"B04",
    "nir":"B8A"
  }
}
```

**Example 2:** If a process needs multiple processes as input, it is allowed to use arrays of the respective types.

``` json
{
  "imagery":{
    "process_id":"union",
    "collection":[
      {
        "process_id":"filter_bands",
        "imagery":{
          "process_id":"get_collection",
          "name":"Sentinel2-L1C"
        },
        "bands":"8"
      },
      {
        "process_id":"filter_bands",
        "imagery":{
          "process_id":"get_collection",
          "name":"Sentinel2-L1C"
        },
        "bands":"5"
      }
    ]
  }
}
```

# Process graphs

_Early work in progress, please contribute by adding [issues](https://github.com/Open-EO/openeo-api-poc/issues)._

## Core processes

There are some processes that we define to be core processes that should be implemented by all back-ends:

### process_graph

Another process graph can be referenced with the process `process_graph`. This could even be an externally hosted process graph.

*Arguments:*

* `uri`: An URI to a process graph.

_Example:_

```
{
  "process_id":"process_graph",
  "args":{
    "uri":"http://otherhost.org/api/v1/users/12345/process_graphs/abcdef"
  }
}
```

# Processes

A process is an operation that performs a specific task, see the [glossary](glossary.md) for a detailed definition. It consists of a name, a set of parameters, a return type and may throw errors or exceptions. In openEO, processes are used to build a chain of processes ([process graph](processgraphs.md)), which can be applied to EO data to derive your own findings from the data.

## Core processes

There are some processes that we define to be core processes that are pre-defined and back-ends SHOULD follow these specifications to be interoperable. Not all processes need to be implemented by all back-ends.

See the **[process reference](processreference.md)** for pre-defined processes.

!!! note    Currently, there are only few defined processes. Those are only meant as an example how future documentation of processes may look like until the core processes get defined in version 0.4.

## Defining processes

Any back-end provider can either implement a set of pre-defined processes (STRONGLY RECOMMENDED) or define new processes for their domain.

To define new processes, back-end providers should know:

* The name is the identifier for the process and MUST never contain a forward slash `/`. 
* Each parameter has a name and the content follows a schema.
* The content returned by a process also follows a schema.
* The schema usually defines the data type and a format according to JSON schema. There are openEO specific formats defined below.

## openEO specific formats

In addition to the native data formats specified by JSON schema, openEO defines a set of specific formats that should be re-used in process schema definitions:

| Format Name       | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| `eodata`          | A proprietary way to pass the processed data from one process to another. |
| `temporal_extent` | A temporal extent as formally specified by the openEO API.   |
| `spatial_extent`  | A spatial extent (with crs) as formally specified by the openEO API. |

!!! note    These formats are still evolving and will likely change with the definition of the openEO processes for openEO API version 0.4.